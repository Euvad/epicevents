# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 16:07:47 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 21:26:53 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.client import Client
from models.contract import Contract
from models.event import Event
from models.user import User
from models.role import Role
from dao.client_dao import ClientDAO
from dao.contract_dao import ContractDAO
from dao.event_dao import EventDAO
from dao.user_dao import UserDAO
from dao.role_dao import RoleDAO
from utils.jwt_utils import generate_jwt, decode_jwt
from utils.authorization import has_permission
from colorama import init, Fore, Style
from config import DATABASE_URL

# Initialize Colorama
init(autoreset=True)

class CustomTestResult(unittest.TextTestResult):
    """Custom test result to print colored output."""
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(Fore.GREEN + "[OK] " + Style.RESET_ALL)
        self.stream.writeln(self.getDescription(test))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(Fore.RED + "[FAILED] " + Style.RESET_ALL)
        self.stream.writeln(self.getDescription(test))
        self.stream.writeln(Fore.RED + self._exc_info_to_string(err, test) + Style.RESET_ALL)

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(Fore.RED + "[ERROR] " + Style.RESET_ALL)
        self.stream.writeln(self.getDescription(test))
        self.stream.writeln(Fore.RED + self._exc_info_to_string(err, test) + Style.RESET_ALL)

    def getDescription(self, test):
        """Return a test description with the class and method name."""
        doc_first_line = test.shortDescription()
        if doc_first_line:
            return f"{test.__class__.__name__}.{test._testMethodName} ({doc_first_line})"
        else:
            return f"{test.__class__.__name__}.{test._testMethodName}"

class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.client_dao = ClientDAO(self.session)
        self.contract_dao = ContractDAO(self.session)
        self.event_dao = EventDAO(self.session)
        self.user_dao = UserDAO(self.session)
        self.role_dao = RoleDAO(self.session)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

class TestClientDAO(BaseTestCase):
    def test_add_client(self):
        """Test adding a new client."""
        client = Client(full_name="John Doe", email="john.doe@example.com", phone="123456789", company_name="Doe Inc.")
        self.client_dao.add_client(client)
        result = self.client_dao.get_client_by_id(client.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.full_name, "John Doe")

    def test_delete_client(self):
        """Test deleting a client."""
        client = Client(full_name="Jane Doe", email="jane.doe@example.com", phone="987654321", company_name="Doe LLC")
        self.client_dao.add_client(client)
        self.client_dao.delete_client(client.id)
        result = self.client_dao.get_client_by_id(client.id)
        self.assertIsNone(result)

class TestContractDAO(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Ensure there is a client to associate contracts with, using unique email
        self.client = Client(full_name="Client One", email="unique_client.one@example.com", phone="123123123", company_name="ClientCo")
        existing_client = self.client_dao.get_client_by_id(self.client.id)
        if not existing_client:
            self.client_dao.add_client(self.client)

    def test_add_contract(self):
        """Test adding a new contract."""
        contract = Contract(client_id=self.client.id, total_amount=1000.0, amount_remaining=500.0, signed=False)
        self.contract_dao.add_contract(contract)
        result = self.contract_dao.get_contract_by_id(contract.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.total_amount, 1000.0)

    def test_update_contract(self):
        """Test updating a contract."""
        contract = Contract(client_id=self.client.id, total_amount=2000.0, amount_remaining=2000.0, signed=False)
        self.contract_dao.add_contract(contract)
        contract.signed = True
        self.contract_dao.update_contract(contract)
        updated_contract = self.contract_dao.get_contract_by_id(contract.id)
        self.assertTrue(updated_contract.signed)

    def test_delete_contract(self):
        """Test deleting a contract."""
        contract = Contract(client_id=self.client.id, total_amount=1500.0, amount_remaining=1500.0, signed=False)
        self.contract_dao.add_contract(contract)
        self.contract_dao.delete_contract(contract.id)
        result = self.contract_dao.get_contract_by_id(contract.id)
        self.assertIsNone(result, "Contract should be None after deletion")

class TestEventDAO(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Ensure there is a contract to associate events with, using unique email
        self.client = Client(full_name="Client Two", email="unique_client.two@example.com", phone="321321321", company_name="ClientTwo")
        existing_client = self.client_dao.get_client_by_id(self.client.id)
        if not existing_client:
            self.client_dao.add_client(self.client)
        self.contract = Contract(client_id=self.client.id, total_amount=2000.0, amount_remaining=2000.0, signed=True)
        self.contract_dao.add_contract(self.contract)

    def test_add_event(self):
        """Test adding a new event."""
        event = Event(contract_id=self.contract.id, client_name="Client Two", client_contact="client.two@example.com",
                      start_date="2024-08-06", end_date="2024-08-07", support_contact="Support Person",
                      location="123 Event St.", attendees=100, notes="Event Notes")
        self.event_dao.add_event(event)
        result = self.event_dao.get_event_by_id(event.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.client_name, "Client Two")

    def test_update_event(self):
        """Test updating an event."""
        event = Event(contract_id=self.contract.id, client_name="Client Three", client_contact="client.three@example.com",
                      start_date="2024-08-08", end_date="2024-08-09", support_contact="Support Staff",
                      location="321 Event Ave.", attendees=150, notes="Another Event")
        self.event_dao.add_event(event)
        event.location = "456 Updated Ave."
        self.event_dao.update_event(event)
        updated_event = self.event_dao.get_event_by_id(event.id)
        self.assertEqual(updated_event.location, "456 Updated Ave.")

    def test_delete_event(self):
        """Test deleting an event."""
        event = Event(contract_id=self.contract.id, client_name="Client Four", client_contact="client.four@example.com",
                      start_date="2024-08-10", end_date="2024-08-11", support_contact="Event Support",
                      location="789 Event Blvd.", attendees=200, notes="Final Event")
        self.event_dao.add_event(event)
        self.event_dao.delete_event(event.id)
        result = self.event_dao.get_event_by_id(event.id)
        self.assertIsNone(result, "Event should be None after deletion")

class TestUserDAO(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Ensure there is a role to assign to users
        existing_role = self.role_dao.get_role_by_name("Admin")
        if existing_role:
            self.role = existing_role
        else:
            self.role = self.role_dao.create_role(name="Admin", permissions="create_client,view_client")

    def test_create_user(self):
        """Test creating a user."""
        user = self.user_dao.create_user(employee_number="1234", name="Alice", email="alice@example.com",
                                         password="password123", department="Sales", role_id=self.role.id)
        result = self.user_dao.get_user_by_email("alice@example.com")
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Alice")

    def test_user_authentication(self):
        """Test user authentication."""
        # Create a user with the existing role
        self.user_dao.create_user(employee_number="5678", name="Bob", email="bob@example.com",
                                  password="password456", department="Management", role_id=self.role.id)
        authenticated_user = self.user_dao.authenticate_user(email="bob@example.com", password="password456")
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.name, "Bob")

    def test_update_user(self):
        """Test updating a user's information."""
        user = self.user_dao.create_user(employee_number="91011", name="Charlie", email="charlie@example.com",
                                         password="password789", department="IT", role_id=self.role.id)
        user.name = "Charlie Brown"
        user.department = "Development"
        updated_user = self.user_dao.update_user(user.id, name=user.name, department=user.department)
        self.assertEqual(updated_user.name, "Charlie Brown")
        self.assertEqual(updated_user.department, "Development")

    def test_delete_user(self):
        """Test deleting a user."""
        user = self.user_dao.create_user(employee_number="1213", name="Dave", email="dave@example.com",
                                         password="password101112", department="HR", role_id=self.role.id)
        self.user_dao.delete_user(user.id)
        result = self.user_dao.get_user_by_email("dave@example.com")
        self.assertIsNone(result)

class TestJWTUtils(unittest.TestCase):
    def test_generate_and_decode_jwt(self):
        """Test generating and decoding JWT."""
        user_id = 1
        token = generate_jwt(user_id)
        decoded_user_id = decode_jwt(token)
        self.assertEqual(user_id, decoded_user_id)

    def test_invalid_jwt(self):
        """Test handling of an invalid JWT."""
        invalid_token = "invalid.token.here"
        with self.assertRaises(Exception) as context:
            decode_jwt(invalid_token)
        self.assertTrue("Invalid token" in str(context.exception))

class TestAuthorizationUtils(BaseTestCase):
    def setUp(self):
        super().setUp()
        # Ensure there is a role with specific permissions
        existing_role = self.role_dao.get_role_by_name("Manager")
        if existing_role:
            self.role = existing_role
        else:
            self.role = self.role_dao.create_role(name="Manager", permissions="create_client,view_client,delete_client")

        # Create a user with the Manager role
        self.user = self.user_dao.create_user(employee_number="5678", name="Bob", email="bob@example.com",
                                              password="password456", department="Management", role_id=self.role.id)

    def test_has_permission(self):
        """Test permission checks."""
        has_create_permission = has_permission(self.user, "create_client")
        self.assertTrue(has_create_permission)

        has_update_permission = has_permission(self.user, "update_client")
        self.assertFalse(has_update_permission)

def run_tests():
    # Run the tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestClientDAO)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestContractDAO))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestEventDAO))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestUserDAO))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestJWTUtils))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestAuthorizationUtils))
    
    # Use the custom test runner
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print(Fore.GREEN + "All tests passed!" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Some tests failed. Failures: {len(result.failures)} Errors: {len(result.errors)}" + Style.RESET_ALL)
        for failed_test, traceback in result.failures:
            print(Fore.RED + f"FAILED: {failed_test}" + Style.RESET_ALL)
            print(traceback)

if __name__ == '__main__':
    run_tests()

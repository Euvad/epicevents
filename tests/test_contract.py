# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_contract.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/08 18:02:48 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 14:41:57 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import unittest
import sys
import os
import uuid

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.event import Event
from models.client import Client
from models.contract import Contract
from dao.client_dao import ClientDAO
from dao.contract_dao import ContractDAO
from config import TEST_DATABASE_URL


def generate_unique_email(base_name="user"):
    """Generate a unique email address using UUID."""
    unique_id = uuid.uuid4()
    return f"{base_name}.{unique_id}@example.com"


class TestContractDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use the PostgreSQL test database URL
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.client_dao = ClientDAO(self.session)
        self.contract_dao = ContractDAO(self.session)

        # Ensure there is a client to associate with contracts
        unique_email = generate_unique_email("test.client")
        self.client = Client(
            full_name="Test Client",
            email=unique_email,
            phone="1234567890",
            company_name="Test Company",
        )
        self.client_dao.add_client(self.client)

        # Clear contracts before each test to ensure isolation
        self.session.query(Contract).delete()
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_add_contract(self):
        """Test adding a new contract."""
        contract = Contract(
            client_id=self.client.id,
            total_amount=1000.0,
            amount_remaining=500.0,
            signed=False,
        )
        self.contract_dao.add_contract(contract)
        result = self.contract_dao.get_contract_by_id(contract.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.total_amount, 1000.0)

    def test_get_all_contracts(self):
        """Test retrieving all contracts."""
        contract1 = Contract(
            client_id=self.client.id,
            total_amount=1000.0,
            amount_remaining=500.0,
            signed=False,
        )
        contract2 = Contract(
            client_id=self.client.id,
            total_amount=2000.0,
            amount_remaining=1500.0,
            signed=True,
        )
        self.contract_dao.add_contract(contract1)
        self.contract_dao.add_contract(contract2)
        result = self.contract_dao.get_all_contracts()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].total_amount, 1000.0)
        self.assertEqual(result[1].total_amount, 2000.0)

    def test_update_contract(self):
        """Test updating a contract."""
        contract = Contract(
            client_id=self.client.id,
            total_amount=1500.0,
            amount_remaining=1500.0,
            signed=False,
        )
        self.contract_dao.add_contract(contract)
        contract.total_amount = 2000.0
        self.contract_dao.update_contract(contract)
        result = self.contract_dao.get_contract_by_id(contract.id)
        self.assertEqual(result.total_amount, 2000.0)


def test_delete_contract(self):
    """Test deleting a contract."""
    contract = Contract(
        client_id=self.client.id,
        total_amount=1200.0,
        amount_remaining=1200.0,
        signed=False,
    )
    self.contract_dao.add_contract(contract)

    # Delete the contract
    self.contract_dao.delete_contract(contract.id)

    # Attempt to retrieve the deleted contract
    result = self.contract_dao.get_contract_by_id(contract.id)

    # Assert that the contract is not found
    self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

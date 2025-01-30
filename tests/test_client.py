# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_client.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/08 18:00:39 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 14:26:56 by Vadim            ###   ########.fr        #
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
from models.contract import Contract
from models.event import Event
from models.client import Client
from dao.client_dao import ClientDAO
from config import TEST_DATABASE_URL


def generate_unique_email(base_name="user"):
    """Génère un email unique en utilisant un UUID."""
    unique_id = uuid.uuid4()
    return f"{base_name}.{unique_id}@example.com"


class TestClientDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.client_dao = ClientDAO(self.session)

        # Explicitly delete all clients before each test to ensure isolation
        self.session.query(Client).delete()
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_add_client(self):
        """Test adding a new client."""
        email = generate_unique_email("john.doe")
        client = Client(
            full_name="John Doe",
            email=email,
            phone="123456789",
            company_name="Doe Inc.",
        )
        self.client_dao.add_client(client)
        result = self.client_dao.get_client_by_id(client.id)
        self.assertIsNotNone(result)
        self.assertEqual(result.full_name, "John Doe")

    def test_get_all_clients(self):
        """Test retrieving all clients."""
        email1 = generate_unique_email("john.doe")
        email2 = generate_unique_email("jane.smith")
        client1 = Client(
            full_name="John Doe",
            email=email1,
            phone="123456789",
            company_name="Doe Inc.",
        )
        client2 = Client(
            full_name="Jane Smith",
            email=email2,
            phone="987654321",
            company_name="Smith LLC",
        )
        self.client_dao.add_client(client1)
        self.client_dao.add_client(client2)
        result = self.client_dao.get_all_clients()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].full_name, "John Doe")
        self.assertEqual(result[1].full_name, "Jane Smith")

    def test_update_client(self):
        """Test updating a client."""
        email = generate_unique_email("john.doe")
        client = Client(
            full_name="John Doe",
            email=email,
            phone="123456789",
            company_name="Doe Inc.",
        )
        self.client_dao.add_client(client)
        client.full_name = "Johnathan Doe"
        self.client_dao.update_client(client)
        result = self.client_dao.get_client_by_id(client.id)
        self.assertEqual(result.full_name, "Johnathan Doe")

    def test_delete_client(self):
        """Test deleting a client."""
        email = generate_unique_email("jane.doe")
        client = Client(
            full_name="Jane Doe", email=email, phone="987654321", company_name="Doe LLC"
        )
        self.client_dao.add_client(client)
        self.client_dao.delete_client(client.id)
        result = self.client_dao.get_client_by_id(client.id)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

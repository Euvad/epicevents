# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_event.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/08 18:03:55 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 14:31:50 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import unittest
import os
import sys
import uuid

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.client import Client
from models.contract import Contract
from models.event import Event
from dao.client_dao import ClientDAO
from dao.contract_dao import ContractDAO
from dao.event_dao import EventDAO
from config import TEST_DATABASE_URL
from datetime import date


def generate_unique_email(base_name="user"):
    """Génère un email unique en utilisant un UUID."""
    unique_id = uuid.uuid4()
    return f"{base_name}.{unique_id}@example.com"


class TestEventDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.client_dao = ClientDAO(self.session)
        self.contract_dao = ContractDAO(self.session)
        self.event_dao = EventDAO(self.session)

        self.session.query(Event).delete()
        self.session.query(Contract).delete()
        self.session.query(Client).delete()
        self.session.commit()

        client_email = generate_unique_email("test.client")
        self.client = Client(
            full_name="Test Client",
            email=client_email,
            phone="1234567890",
            company_name="Test Company",
        )
        self.client_dao.add_client(self.client)
        self.contract = Contract(
            client_id=self.client.id,
            total_amount=1000.0,
            amount_remaining=500.0,
            signed=True,
        )
        self.contract_dao.add_contract(self.contract)

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_add_event(self):
        """Test adding a new event."""
        event = Event(
            contract_id=self.contract.id,
            start_date=date(2024, 8, 10),  # Utilisation de datetime.date
            end_date=date(2024, 8, 11),
            support_contact="Support Contact",
            location="Test Location",
            attendees=100,
            notes="Test Notes",
        )
        self.event_dao.add_event(event)
        result = self.event_dao.get_event_by_id(event.id)
        self.assertIsNotNone(result)

    def test_get_all_events(self):
        """Test retrieving all events."""
        event1 = Event(
            contract_id=self.contract.id,
            start_date=date(2024, 8, 10),
            end_date=date(2024, 8, 11),
            support_contact="Support Contact",
            location="Test Location",
            attendees=100,
            notes="Test Notes",
        )
        event2 = Event(
            contract_id=self.contract.id,
            start_date=date(2024, 9, 10),
            end_date=date(2024, 9, 11),
            support_contact="Support Contact 2",
            location="Test Location 2",
            attendees=200,
            notes="Test Notes 2",
        )
        self.event_dao.add_event(event1)
        self.event_dao.add_event(event2)
        result = self.event_dao.get_all_events()
        self.assertEqual(len(result), 2)

    def test_update_event(self):
        """Test updating an event."""
        event = Event(
            contract_id=self.contract.id,
            start_date=date(2024, 8, 10),
            end_date=date(2024, 8, 11),
            support_contact="Support Contact",
            location="Test Location",
            attendees=100,
            notes="Test Notes",
        )
        self.event_dao.add_event(event)
        event.location = "Updated Location"
        self.event_dao.update_event(event)
        result = self.event_dao.get_event_by_id(event.id)
        self.assertEqual(result.location, "Updated Location")

    def test_delete_event(self):
        """Test deleting an event."""
        event = Event(
            contract_id=self.contract.id,
            start_date=date(2024, 8, 10),
            end_date=date(2024, 8, 11),
            support_contact="Support Contact",
            location="Test Location",
            attendees=100,
            notes="Test Notes",
        )
        self.event_dao.add_event(event)
        self.event_dao.delete_event(event.id)
        with self.assertRaises(Exception):
            self.event_dao.get_event_by_id(event.id)


if __name__ == "__main__":
    unittest.main()

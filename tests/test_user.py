# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_user.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/08 18:06:41 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 14:36:48 by Vadim            ###   ########.fr        #
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
from models.user import User
from dao.user_dao import UserDAO
from config import TEST_DATABASE_URL


def generate_unique_email(base_name="user"):
    """Génère un email unique en utilisant un UUID."""
    unique_id = uuid.uuid4()
    return f"{base_name}.{unique_id}@example.com"


class TestUserDAO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.user_dao = UserDAO(self.session)
        # Clear users before each test
        self.session.query(User).delete()
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)
        cls.engine.dispose()

    def test_create_user(self):
        """Test creating a new user."""
        email = generate_unique_email("alice")
        user = self.user_dao.create_user(
            employee_number="1234",
            name="Alice",
            email=email,
            password="password123",
            role="Sales",
        )
        result = self.user_dao.get_user_by_email(email)
        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Alice")

    def test_get_user_by_email(self):
        """Test retrieving a user by their email."""
        email = generate_unique_email("bob")
        self.user_dao.create_user(
            employee_number="5678",
            name="Bob",
            email=email,
            password="password456",
            role="Management",
        )
        user = self.user_dao.get_user_by_email(email)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Bob")

    def test_update_user(self):
        """Test updating a user's information."""
        email = generate_unique_email("charlie")
        user = self.user_dao.create_user(
            employee_number="91011",
            name="Charlie",
            email=email,
            password="password789",
            role="IT",
        )
        user.name = "Charlie Brown"
        user.role = "Development"
        updated_user = self.user_dao.update_user(
            user.id, name=user.name, role=user.role
        )
        self.assertEqual(updated_user.name, "Charlie Brown")
        self.assertEqual(updated_user.role, "Development")

    def test_delete_user(self):
        """Test deleting a user by their ID."""
        email = generate_unique_email("dave")
        user = self.user_dao.create_user(
            employee_number="1213",
            name="Dave",
            email=email,
            password="password101112",
            role="HR",
        )
        self.user_dao.delete_user(user.id)
        result = self.user_dao.get_user_by_email(email)
        self.assertIsNone(result)

    def test_user_authentication(self):
        """Test user authentication."""
        email = generate_unique_email("eve")
        self.user_dao.create_user(
            employee_number="5678",
            name="Eve",
            email=email,
            password="password456",
            role="Management",
        )
        authenticated_user = self.user_dao.authenticate_user(
            email=email, password="password456"
        )
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.name, "Eve")


if __name__ == "__main__":
    unittest.main()

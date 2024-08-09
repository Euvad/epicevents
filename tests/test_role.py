# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_role.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/08 18:04:56 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 14:12:53 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)
import unittest
from database import engine, Session  # Adjust imports as needed
from models.base import Base
from models.role import Role
from models.user import User  # Ensure these imports are correct
from dao.role_dao import RoleDAO  # Ensure RoleDAO is correctly implemented


class TestRoleDAO(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(engine)

    def setUp(self):
        self.session = Session()
        self.role_dao = RoleDAO(self.session)

        # Clear existing data for isolated tests
        self.session.query(Role).delete()
        self.session.commit()

    def tearDown(self):
        self.session.rollback()
        self.session.close()

    def test_create_role(self):
        role = self.role_dao.create_role(name="Test Role", permissions="read,write")
        self.assertEqual(role.name, "Test Role")
        self.assertEqual(role.permissions, "read,write")

    def test_get_role_by_name(self):
        self.role_dao.create_role(name="Test Role", permissions="read")
        role = self.role_dao.get_role_by_name("Test Role")
        self.assertIsNotNone(role)
        self.assertEqual(role.name, "Test Role")
        self.assertEqual(role.permissions, "read")

    def test_update_role(self):
        role = self.role_dao.create_role(name="Test Role", permissions="read")
        role.name = "Updated Role"
        role.permissions = "write"
        updated_role = self.role_dao.update_role(role)
        self.assertEqual(updated_role.name, "Updated Role")
        self.assertEqual(updated_role.permissions, "write")

    def test_delete_role(self):
        role = self.role_dao.create_role(name="Test Role", permissions="read")
        self.role_dao.delete_role(role)
        deleted_role = self.role_dao.get_role_by_name("Test Role")
        self.assertIsNone(deleted_role)


if __name__ == "__main__":
    unittest.main()

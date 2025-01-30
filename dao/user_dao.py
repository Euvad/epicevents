# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    user_dao.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:23:50 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 11:07:58 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User
from utils.security import hash_password, verify_password


class UserDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, employee_number, name, email, password, role):
        """Create a new user with a hashed password."""
        password_hash = hash_password(password)
        user = User(
            employee_number=employee_number,
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,  # Updated to match the new column-based role
        )
        try:
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"User creation failed: {e.orig.diag.message_detail}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error creating user: {e}")

    def get_user_by_email(self, email) -> User:
        """Retrieve a user by their email."""
        try:
            return self.session.query(User).filter(User.email == email).first()
        except Exception as e:
            raise Exception(f"Error retrieving user by email: {e}")
    def get_user_by_id(self, id) -> User:
        """Retrieve a user by their id."""
        try:
            return self.session.query(User).filter(User.id == id).first()
        except Exception as e:
            raise Exception(f"Error retrieving user by id: {e}")      
    def authenticate_user(self, email, password) -> User:
        """Authenticate a user by verifying their password."""
        try:
            user = self.get_user_by_email(email)
            if user and verify_password(user.password_hash, password):
                return user
            return None
        except Exception as e:
            raise Exception(f"Error authenticating user: {e}")

    def update_user(
        self,
        user_id,
        name=None,
        email=None,
        password=None,
        role=None,  # Updated to match the new column-based role
    ):
        """Update an existing user's information."""
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                raise Exception("User not found")

            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            if password is not None:
                user.password_hash = hash_password(password)
            if role is not None:
                user.role = role

            self.session.commit()
            return user
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"User update failed: {e.orig.diag.message_detail}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error updating user: {e}")

    def delete_user(self, user_id):
        """Delete a user by their ID."""
        try:
            user = self.session.query(User).filter(User.id == user_id).first()
            if not user:
                raise Exception("User not found")

            self.session.delete(user)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error deleting user: {e}")
    def get_all_users(self) -> list[User]:
        """Retrieve all users."""
        try:
            return self.session.query(User).all()
        except Exception as e:
            raise Exception(f"Error retrieving all users: {e}")

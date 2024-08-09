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

    def create_user(self, employee_number, name, email, password, department, role_id):
        """Create a new user with a hashed password."""
        password_hash = hash_password(password)
        user = User(
            employee_number=employee_number,
            name=name,
            email=email,
            password_hash=password_hash,
            department=department,
            role_id=role_id,
        )
        try:
            self.session.add(user)
            self.session.commit()
            return user
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"User creation failed: {e.orig.diag.message_detail}")

    def get_user_by_email(self, email) -> User:
        """Retrieve a user by their email."""
        return self.session.query(User).filter(User.email == email).first()

    def authenticate_user(self, email, password) -> User:
        """Authenticate a user by verifying their password."""
        user = self.get_user_by_email(email)
        if user and verify_password(user.password_hash, password):
            return user
        return None

    def update_user(
        self,
        user_id,
        name=None,
        email=None,
        password=None,
        department=None,
        role_id=None,
    ):
        """Update an existing user's information."""
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("User not found")

        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if password is not None:
            user.password_hash = hash_password(password)
        if department is not None:
            user.department = department
        if role_id is not None:
            user.role_id = role_id

        try:
            self.session.commit()
            return user
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"User update failed: {e.orig.diag.message_detail}")

    def delete_user(self, user_id):
        """Delete a user by their ID."""
        user = self.session.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("User not found")

        self.session.delete(user)
        self.session.commit()

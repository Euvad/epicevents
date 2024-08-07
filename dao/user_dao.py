# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    user_dao.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:23:50 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:23:54 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session
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
            role_id=role_id
        )
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_email(self, email) -> User:
        """Retrieve a user by their email."""
        return self.session.query(User).filter(User.email == email).first()

    def authenticate_user(self, email, password) -> User:
        """Authenticate a user by verifying their password."""
        user = self.get_user_by_email(email)
        if user and verify_password(user.password_hash, password):
            return user
        return None

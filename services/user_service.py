# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    user_service.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 20:30:29 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 20:36:04 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dao.user_dao import UserDAO
from utils.validation import validate_non_empty_string
from utils.authorization import has_permission

class UserService:
    def __init__(self, session):
        self.user_dao = UserDAO(session)

    def create_user(self, current_user, employee_number, name, email, password, department, role_id):
        # Check permission
        has_permission(current_user, 'create_user')

        # Validate input data
        validate_non_empty_string(employee_number, 'Employee Number')
        validate_non_empty_string(name, 'Name')
        validate_non_empty_string(email, 'Email')
        validate_non_empty_string(password, 'Password')
        validate_non_empty_string(department, 'Department')

        # Create user
        return self.user_dao.create_user(employee_number, name, email, password, department, role_id)

    def update_user(self, current_user, user_id, name=None, email=None, department=None, role_id=None):
        # Check permission
        has_permission(current_user, 'update_user')

        # Validate input data
        if name is not None:
            validate_non_empty_string(name, 'Name')
        if email is not None:
            validate_non_empty_string(email, 'Email')
        if department is not None:
            validate_non_empty_string(department, 'Department')

        # Update user
        return self.user_dao.update_user(user_id, name, email, department, role_id)

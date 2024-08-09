# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    auth_service.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:33:20 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:33:23 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dao.user_dao import UserDAO
from utils.jwt_utils import generate_jwt


class AuthService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def login(self, email, password):
        user = self.user_dao.authenticate_user(email, password)
        if user:
            token = generate_jwt(user.id)
            return token
        else:
            raise Exception("Invalid email or password")

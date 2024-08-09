# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    authorization_service.py                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:33:59 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:34:02 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from dao.user_dao import UserDAO
from utils.authorization import has_permission


class AuthorizationService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def check_permission(self, user_id, permission):
        user = self.user_dao.get_user_by_id(user_id)
        if not user or not has_permission(user, permission):
            raise Exception("Unauthorized: Insufficient permissions")

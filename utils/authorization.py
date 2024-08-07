# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    authorization.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:21:35 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:21:37 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

def has_permission(user, permission):
    role_permissions = user.role.permissions.split(',')
    return permission in role_permissions

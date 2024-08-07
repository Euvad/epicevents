# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    security.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:20:56 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:21:00 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(password):
    """Hash a password for storing."""
    return ph.hash(password)

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by the user."""
    try:
        ph.verify(stored_password, provided_password)
        return True
    except Exception:
        return False

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    jwt_utils.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:31:35 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:51:23 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import jwt
from datetime import datetime, timedelta
from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS

def generate_jwt(user_id):
    """Generate a JSON Web Token for a user."""
    exp = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    payload = {'user_id': user_id, 'exp': exp}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt(token):
    """Decode a JSON Web Token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

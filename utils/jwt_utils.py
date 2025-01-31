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
    # Calcul du temps d'expiration du token en ajoutant une durée définie par JWT_EXP_DELTA_SECONDS
    exp = datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    
    # Création du payload contenant l'ID de l'utilisateur et l'heure d'expiration
    payload = {"user_id": user_id, "exp": exp}
    
    # Génération du token avec le payload, la clé secrète et l'algorithme de signature définis dans la configuration
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt(token):
    """Decode a JSON Web Token."""
    try:
        # Décode le token en utilisant la clé secrète et l'algorithme spécifié dans la configuration
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        # Retourne l'ID de l'utilisateur contenu dans le token
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        # Si le token a expiré, lève une exception avec un message approprié
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        # Si le token est invalide pour toute autre raison, lève une exception avec un message approprié
        raise Exception("Invalid token")

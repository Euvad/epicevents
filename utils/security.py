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

# Initialise le mot de passe hashé avec la bibliothèque Argon2
ph = PasswordHasher()


def hash_password(password):
    """Hash a password for storing."""
    # La fonction `hash` applique un algorithme de hachage sécurisé (Argon2) sur le mot de passe pour le sécuriser.
    # Cela permet de stocker un mot de passe sécurisé sans jamais le sauvegarder en texte brut.
    return ph.hash(password)


def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by the user."""
    try:
        # Vérifie si le mot de passe fourni correspond au mot de passe stocké après l'avoir hashé
        ph.verify(stored_password, provided_password)
        return True  # Si la vérification réussit, retourne True
    except Exception:
        # Si la vérification échoue (par exemple, le mot de passe ne correspond pas), retourne False
        return False

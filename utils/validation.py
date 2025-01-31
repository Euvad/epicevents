# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    validation.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 20:27:36 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 21:31:13 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from datetime import datetime, date
import re
from typing import Optional  # Use Optional for typing compatibility


# Validation utility functions
def validate_email(email: str) -> bool:
    """Validate email format using a regex pattern."""
    # Expression régulière pour valider l'email selon un format standard (ex. : exemple@domaine.com)
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$"
    # La fonction re.match vérifie si l'email respecte le format défini dans la regex
    return re.match(email_regex, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number to be digits only and have a valid length."""
    # Vérifie si le numéro de téléphone est composé uniquement de chiffres et s'il a une longueur valide (au moins 10 chiffres)
    return phone.isdigit() and len(phone) >= 10


def validate_amount(amount: float) -> bool:
    """Ensure the amount is a positive number."""
    # Vérifie que le montant est un nombre positif
    return amount > 0


def validate_signed(signed: str) -> bool:
    """Ensure the signed input is 'yes' or 'no'."""
    # Vérifie si la valeur entrée est 'yes' ou 'no', ce qui est utile pour valider un champ binaire
    return signed.lower() in ["yes", "no"]


def parse_date(dt: str) -> Optional[date]:
    """Try to parse a string into a date, return None if invalid."""
    try:
        # Tente de convertir une chaîne de caractères au format 'YYYY-MM-DD' en objet date
        return datetime.strptime(dt, "%Y-%m-%d").date()
    except ValueError:
        # Si la chaîne n'est pas dans le bon format, retourne None
        return None

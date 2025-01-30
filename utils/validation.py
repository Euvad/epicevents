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
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$"
    return re.match(email_regex, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number to be digits only and have a valid length."""
    return phone.isdigit() and len(phone) >= 10


def validate_amount(amount: float) -> bool:
    """Ensure the amount is a positive number."""
    return amount > 0


def validate_signed(signed: str) -> bool:
    """Ensure the signed input is 'yes' or 'no'."""
    return signed.lower() in ["yes", "no"]


def parse_date(dt: str) -> Optional[date]:
    try:
        return datetime.strptime(dt, "%Y-%m-%d").date()
    except ValueError:
        return None

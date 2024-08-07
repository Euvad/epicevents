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

from datetime import datetime
import re


def validate_email(email):
    """Validate email address format."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def validate_phone(phone):
    """Validate phone number format (simple version)."""
    regex = r'^\d{10}$'  # Assumes 10-digit phone numbers
    return re.match(regex, phone)

def validate_non_empty_string(value, field_name):
    if not value or not isinstance(value, str) or value.strip() == "":
        raise ValueError(f"{field_name} must be a non-empty string")

def validate_positive_number(value, field_name):
    if value is None or not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{field_name} must be a positive number")

def validate_date_string(date_str, field_name):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"{field_name} must be a valid date in YYYY-MM-DD format")

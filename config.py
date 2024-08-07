# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:30:22 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:30:25 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# JWT configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXP_DELTA_SECONDS = int(os.getenv('JWT_EXP_DELTA_SECONDS', 3600))

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL')

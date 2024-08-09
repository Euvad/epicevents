# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    sentry.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/09 15:07:25 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 15:09:45 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sentry_sdk
from config import SENTRY_DSN

def call_sentry():
    sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

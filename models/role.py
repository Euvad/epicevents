# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    role.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:18:05 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 10:56:05 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    permissions = Column(
        String
    )  # Permissions can be stored as a JSON string or a comma-separated string

    # Relationships
    users = relationship("User", back_populates="role")

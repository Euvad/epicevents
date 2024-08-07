# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    user.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:17:39 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:17:48 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    department = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)

    # Relationships
    role = relationship('Role', back_populates='users')

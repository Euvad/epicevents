# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    client.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:10:13 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 11:34:56 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    company_name = Column(String)  # nullable
    creation_date = Column(Date)
    last_contact_date = Column(Date)
    # commercial_contact = Column(String)#relier a un user commercant relationship
    commercial_contact = Column(Integer, ForeignKey("users.id"), nullable=True)
    # Relationships
    contracts = relationship("Contract", back_populates="client")
    commercial = relationship("User")

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    contract.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:10:33 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:10:39 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    total_amount = Column(Float, nullable=False)
    amount_remaining = Column(Float, nullable=False)
    creation_date = Column(Date)
    signed = Column(Boolean, default=False)

    client = relationship("Client", back_populates="contracts")
    commercial = relationship("User")  # Relation avec User (Commercial)
    events = relationship("Event", back_populates="contract")
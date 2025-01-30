# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    event.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:10:48 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:10:51 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    support_contact = Column(String, nullable=True)  # Peut être null
    location = Column(String, nullable=True)
    attendees = Column(Integer, nullable=True, default=0)
    notes = Column(String, nullable=True)  # Peut être null

    # Relations
    contract = relationship("Contract", back_populates="events")

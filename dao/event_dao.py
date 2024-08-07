# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    event_dao.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:23:31 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 20:26:52 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.event import Event

class EventDAO:
    def __init__(self, session: Session):
        self.session = session

    def add_event(self, event: Event):
        """Add a new event."""
        try:
            self.session.add(event)
            self.session.commit()
            return event
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"Event creation failed: {e.orig.diag.message_detail}")

    def get_event_by_id(self, event_id: int) -> Event:
        """Retrieve an event by its ID."""
        event = self.session.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise Exception("Event not found")
        return event

    def get_all_events(self) -> list[Event]:
        """Retrieve all events."""
        return self.session.query(Event).all()

    def update_event(self, event: Event):
        """Update an existing event's details."""
        existing_event = self.get_event_by_id(event.id)
        if existing_event:
            existing_event.client_name = event.client_name
            existing_event.client_contact = event.client_contact
            existing_event.start_date = event.start_date
            existing_event.end_date = event.end_date
            existing_event.support_contact = event.support_contact
            existing_event.location = event.location
            existing_event.attendees = event.attendees
            existing_event.notes = event.notes
            try:
                self.session.commit()
                return existing_event
            except IntegrityError as e:
                self.session.rollback()
                raise Exception(f"Event update failed: {e.orig.diag.message_detail}")

    def delete_event(self, event_id: int):
        """Delete an event."""
        event = self.get_event_by_id(event_id)
        if event:
            try:
                self.session.delete(event)
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                raise Exception(f"Event deletion failed: {e.orig.diag.message_detail}")

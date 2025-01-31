from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.event import Event


class EventDAO:
    def __init__(self, session: Session):
        # Initialisation du DAO avec une session SQLAlchemy, permettant l'interaction avec la base de données.
        self.session = session

    def add_event(self, event: Event):
        """Add a new event."""
        try:
            # Ajout d'un événement à la session (la transaction n'est pas encore validée à ce point)
            self.session.add(event)
            self.session.commit()  # Validation de la transaction dans la base de données
            return event  # Retourne l'événement ajouté
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit (par exemple, violation de contrainte unique), la transaction est annulée
            self.session.rollback()
            raise  # Relance l'exception pour la gestion ultérieure
        except Exception as e:
            # Gère toutes autres erreurs non spécifiées
            self.session.rollback()
            raise Exception(f"Error adding event: {e}")  # Relance l'exception après rollback

    def get_event_by_id(self, event_id: int) -> Event:
        """Retrieve an event by its ID."""
        try:
            # Récupère un événement par son ID, en filtrant par l'ID dans la base de données
            event = self.session.query(Event).filter(Event.id == event_id).first()
            if not event:
                # Si aucun événement n'est trouvé, lève une exception
                raise Exception("Event not found")
            return event  # Retourne l'événement trouvé
        except Exception as e:
            # Gère toutes les exceptions survenues pendant la récupération de l'événement
            raise Exception(f"Error retrieving event by ID: {e}")  # Relance l'exception après avoir signalé l'erreur

    def get_all_events(self) -> list[Event]:
        """Retrieve all events."""
        try:
            # Récupère tous les événements présents dans la base de données
            return self.session.query(Event).all()
        except Exception as e:
            # Gère toute erreur de récupération des événements
            raise Exception(f"Error retrieving all events: {e}")

    def update_event(self, event_id, start_date, end_date, support_contact, location, attendees, notes):
        """Update an existing event's details."""
        try:
            # Récupère l'événement existant à partir de son ID
            existing_event = self.get_event_by_id(event_id)
            if not existing_event:
                raise Exception("Event not found")  # Si l'événement n'est pas trouvé, une exception est levée

            # Mise à jour des attributs de l'événement
            existing_event.start_date = start_date
            existing_event.end_date = end_date
            existing_event.support_contact = support_contact
            existing_event.location = location
            existing_event.attendees = attendees
            existing_event.notes = notes

            # Commit des changements dans la base de données
            self.session.commit()
            return existing_event  # Retourne l'événement mis à jour
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit, rollback et levée de l'exception avec message d'erreur détaillé
            self.session.rollback()
            raise Exception(f"Event update failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Gère toutes autres erreurs non spécifiées
            self.session.rollback()
            raise Exception(f"Error updating event: {e}")

    def delete_event(self, event_id: int):
        """Delete an event."""
        try:
            # Récupère l'événement à supprimer
            event = self.get_event_by_id(event_id)
            if not event:
                raise Exception("Event not found")  # Si l'événement n'est pas trouvé, une exception est levée

            # Supprime l'événement de la session
            self.session.delete(event)
            self.session.commit()  # Commit pour valider la suppression
        except IntegrityError as e:
            # En cas d'erreur d'intégrité (par exemple, si l'événement est référencé ailleurs), rollback
            self.session.rollback()
            raise Exception(f"Event deletion failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Gère toutes autres erreurs de suppression
            self.session.rollback()
            raise Exception(f"Error deleting event: {e}")

    def get_events_for_support(self, support_user_id):
        """Retrieve events assigned to a specific support user."""
        try:
            # Récupère les événements assignés à un utilisateur de support spécifique (en fonction de l'ID)
            return (
                self.session.query(Event)
                .filter(Event.support_contact == support_user_id)  # Filtre par le contact de support affecté
                .all()
            )
        except Exception as e:
            # Gère toute erreur de récupération d'événements pour un utilisateur de support spécifique
            raise Exception(f"Error retrieving events for support: {e}")

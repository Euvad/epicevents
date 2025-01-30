# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    client_dao.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:22:52 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 15:22:56 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session
from models.client import Client


class ClientDAO:
    def __init__(self, session: Session):
        self.session = session

    def add_client(self, client: Client):
        """Add a new client."""
        try:
            self.session.add(client)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error adding client: {e}")

    def get_client_by_id(self, client_id: int) -> Client | None:
        """Retrieve a client by their ID."""
        try:
            return self.session.query(Client).filter(Client.id == client_id).first()
        except Exception as e:
            raise Exception(f"Error retrieving client by ID: {e}")

    def get_all_clients(self) -> list[Client]:
        """Retrieve all clients."""
        try:
            return self.session.query(Client).all()
        except Exception as e:
            raise Exception(f"Error retrieving all clients: {e}")

    def update_client(self, client_id, full_name, email, phone, company_name):
        """Update an existing client's information."""
        try:
            existing_client = self.get_client_by_id(client_id)
            if not existing_client:
                raise Exception("Client not found")

            existing_client.full_name = full_name
            existing_client.email = email
            existing_client.phone = phone
            existing_client.company_name = company_name
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error updating client: {e}")

    def delete_client(self, client_id: int):
        """Delete a client."""
        try:
            client = self.get_client_by_id(client_id)
            if not client:
                raise Exception("Client not found")

            self.session.delete(client)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error deleting client: {e}")

    def add_client_from_params(
        self, name: str, email: str, phone: str, company: str, commercial_contact: int
    ):
        """Add a client directly from parameters, including the assigned commercial."""
        try:
            client = Client(
                full_name=name,
                email=email,
                phone=phone,
                company_name=company,
                commercial_contact=commercial_contact,  # On ajoute l'attribution automatique
            )
            self.session.add(client)
            self.session.commit()
            return client
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error adding client: {e}")

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
        self.session.add(client)
        self.session.commit()

    def get_client_by_id(self, client_id: int) -> Client:
        """Retrieve a client by their ID."""
        return self.session.query(Client).filter(Client.id == client_id).first()

    def get_all_clients(self) -> list[Client]:
        """Retrieve all clients."""
        return self.session.query(Client).all()

    def update_client(self, client: Client):
        """Update an existing client's information."""
        existing_client = self.get_client_by_id(client.id)
        if existing_client:
            existing_client.full_name = client.full_name
            existing_client.email = client.email
            existing_client.phone = client.phone
            existing_client.company_name = client.company_name
            self.session.commit()

    def delete_client(self, client_id: int):
        """Delete a client."""
        client = self.get_client_by_id(client_id)
        if client:
            self.session.delete(client)
            self.session.commit()

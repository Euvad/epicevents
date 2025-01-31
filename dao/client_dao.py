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
        # Initialisation du DAO avec une session SQLAlchemy permettant d'interagir avec la base de données.
        self.session = session

    def add_client(self, client: Client):
        """Add a new client."""
        try:
            # Ajout du client à la session. La transaction n'est pas encore validée ici.
            self.session.add(client)
            self.session.commit()  # Validation de la transaction dans la base de données
        except Exception as e:
            # Si une erreur se produit, on effectue un rollback pour annuler la transaction en cours
            self.session.rollback()
            raise Exception(f"Error adding client: {e}")  # Relance l'exception avec un message d'erreur

    def get_client_by_id(self, client_id: int) -> Client | None:
        """Retrieve a client by their ID."""
        try:
            # Recherche d'un client par son ID. La méthode `first()` retourne None si aucun client n'est trouvé.
            return self.session.query(Client).filter(Client.id == client_id).first()
        except Exception as e:
            # Gestion des erreurs survenues lors de la récupération du client
            raise Exception(f"Error retrieving client by ID: {e}")

    def get_all_clients(self) -> list[Client]:
        """Retrieve all clients."""
        try:
            # Récupère tous les clients dans la base de données
            return self.session.query(Client).all()
        except Exception as e:
            # Gestion des erreurs pendant la récupération de tous les clients
            raise Exception(f"Error retrieving all clients: {e}")

    def update_client(self, client_id, full_name, email, phone, company_name):
        """Update an existing client's information."""
        try:
            # Recherche du client à mettre à jour
            existing_client = self.get_client_by_id(client_id)
            if not existing_client:
                # Si le client n'existe pas, une exception est levée
                raise Exception("Client not found")

            # Mise à jour des informations du client
            existing_client.full_name = full_name
            existing_client.email = email
            existing_client.phone = phone
            existing_client.company_name = company_name

            # Commit des modifications dans la base de données
            self.session.commit()
        except Exception as e:
            # Si une erreur se produit, annule la transaction en cours
            self.session.rollback()
            raise Exception(f"Error updating client: {e}")

    def delete_client(self, client_id: int):
        """Delete a client."""
        try:
            # Recherche du client à supprimer
            client = self.get_client_by_id(client_id)
            if not client:
                # Si le client n'existe pas, une exception est levée
                raise Exception("Client not found")

            # Suppression du client de la base de données
            self.session.delete(client)
            self.session.commit()  # Validation de la suppression
        except Exception as e:
            # Si une erreur se produit, annule la transaction en cours
            self.session.rollback()
            raise Exception(f"Error deleting client: {e}")

    def add_client_from_params(
        self, name: str, email: str, phone: str, company: str, commercial_contact: int
    ):
        """Add a client directly from parameters, including the assigned commercial."""
        try:
            # Création d'un nouvel objet client avec les paramètres fournis, incluant l'attribution du commercial
            client = Client(
                full_name=name,
                email=email,
                phone=phone,
                company_name=company,
                commercial_contact=commercial_contact,  # On attribue un contact commercial automatiquement
            )
            self.session.add(client)  # Ajout du client à la session
            self.session.commit()  # Validation de l'ajout
            return client  # Retourne le client ajouté
        except Exception as e:
            # Si une erreur se produit, annule la transaction en cours
            self.session.rollback()
            raise Exception(f"Error adding client: {e}")

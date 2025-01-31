# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    contract_dao.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:23:13 by Vadim             #+#    #+#              #
#    Updated: 2024/08/07 20:24:33 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.contract import Contract


class ContractDAO:
    def __init__(self, session: Session):
        # Initialisation du DAO avec une session SQLAlchemy permettant d'interagir avec la base de données.
        self.session = session

    def add_contract(self, contract: Contract):
        """Add a new contract."""
        try:
            # Ajout du contrat à la session (la transaction n'est pas encore validée)
            self.session.add(contract)
            self.session.commit()  # Validation de la transaction dans la base de données
            return contract  # Retourne le contrat créé
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit (par exemple, violation de contrainte unique), annule la transaction
            self.session.rollback()
            raise Exception(f"Contract creation failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Gère toutes autres erreurs non spécifiées
            self.session.rollback()
            raise Exception(f"Error adding contract: {e}")

    def get_contract_by_id(self, contract_id: int) -> Contract:
        """Retrieve a contract by its ID."""
        try:
            # Récupère un contrat par son ID
            contract = (
                self.session.query(Contract).filter(Contract.id == contract_id).first()
            )
            if not contract:
                # Si aucun contrat n'est trouvé, une exception est levée
                raise Exception("Contract not found")
            return contract  # Retourne le contrat trouvé
        except Exception as e:
            # Gère toutes les exceptions pendant la récupération du contrat
            raise Exception(f"Error retrieving contract by ID: {e}")

    def get_all_contracts(self) -> list[Contract]:
        """Retrieve all contracts."""
        try:
            # Récupère tous les contrats dans la base de données
            return self.session.query(Contract).all()
        except Exception as e:
            # Gère toute erreur qui pourrait survenir lors de la récupération de tous les contrats
            raise Exception(f"Error retrieving all contracts: {e}")

    def update_contract(self, contract_id, total_amount, amount_remaining, signed):
        """Update an existing contract's details."""
        try:
            # Récupère le contrat existant à partir de son ID
            existing_contract = self.get_contract_by_id(contract_id)
            if not existing_contract:
                # Si le contrat n'est pas trouvé, une exception est levée
                raise Exception("Contract not found")

            # Mise à jour des détails du contrat
            existing_contract.total_amount = total_amount
            existing_contract.amount_remaining = amount_remaining
            existing_contract.signed = signed

            # Validation des changements dans la base de données
            self.session.commit()
            return existing_contract  # Retourne le contrat mis à jour
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit, annule la transaction
            self.session.rollback()
            raise Exception(f"Contract update failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Gère toutes autres erreurs non spécifiées
            self.session.rollback()
            raise Exception(f"Error updating contract: {e}")


    def delete_contract(self, contract_id: int):
        """Delete a contract."""
        try:
            # Récupère le contrat par son ID
            contract = self.get_contract_by_id(contract_id)
            if not contract:
                # Si le contrat n'est pas trouvé, une exception est levée
                raise Exception("Contract not found")

            # Supprime le contrat de la base de données
            self.session.delete(contract)
            self.session.commit()  # Validation de la suppression dans la base de données
        except IntegrityError as e:
            # Si une erreur d'intégrité se produit (par exemple, si le contrat est référencé ailleurs), annule la transaction
            self.session.rollback()
            raise Exception(f"Contract deletion failed: {e.orig.diag.message_detail}")
        except Exception as e:
            # Gère toutes autres erreurs qui pourraient se produire pendant la suppression
            self.session.rollback()
            raise Exception(f"Error deleting contract: {e}")

    def get_unsigned_contracts(self, commercial_id):
        """Retrieve all unsigned contracts for a specific commercial."""
        try:
            # Récupère tous les contrats non signés pour un commercial spécifique
            return (
                self.session.query(Contract)
                .filter(
                    Contract.signed == False,  # Filtre les contrats non signés
                    Contract.client.has(
                        commercial_contact=commercial_id  # Filtre par le contact commercial
                    ),
                )
                .all()
            )
        except Exception as e:
            # Gère les erreurs de récupération des contrats non signés
            raise Exception(f"Error retrieving unsigned contracts: {e}")

    def get_unpaid_contracts(self, commercial_id):
        """Retrieve all unpaid contracts for a specific commercial."""
        try:
            # Récupère tous les contrats non payés pour un commercial spécifique
            return (
                self.session.query(Contract)
                .filter(
                    Contract.amount_remaining > 0,  # Filtre les contrats avec un solde restant
                    Contract.client.has(
                        commercial_contact=commercial_id  # Filtre par le contact commercial
                    ),
                )
                .all()
            )
        except Exception as e:
            # Gère les erreurs de récupération des contrats impayés
            raise Exception(f"Error retrieving unpaid contracts: {e}")

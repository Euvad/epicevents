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
        self.session = session

    def add_contract(self, contract: Contract):
        """Add a new contract."""
        try:
            self.session.add(contract)
            self.session.commit()
            return contract
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"Contract creation failed: {e.orig.diag.message_detail}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error adding contract: {e}")

    def get_contract_by_id(self, contract_id: int) -> Contract:
        """Retrieve a contract by its ID."""
        try:
            contract = (
                self.session.query(Contract).filter(Contract.id == contract_id).first()
            )
            if not contract:
                raise Exception("Contract not found")
            return contract
        except Exception as e:
            raise Exception(f"Error retrieving contract by ID: {e}")

    def get_all_contracts(self) -> list[Contract]:
        """Retrieve all contracts."""
        try:
            return self.session.query(Contract).all()
        except Exception as e:
            raise Exception(f"Error retrieving all contracts: {e}")

    def update_contract(self, contract: Contract):
        """Update an existing contract's details."""
        try:
            existing_contract = self.get_contract_by_id(contract.id)
            if not existing_contract:
                raise Exception("Contract not found")

            existing_contract.total_amount = contract.total_amount
            existing_contract.amount_remaining = contract.amount_remaining
            existing_contract.signed = contract.signed
            self.session.commit()
            return existing_contract
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"Contract update failed: {e.orig.diag.message_detail}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error updating contract: {e}")

    def delete_contract(self, contract_id: int):
        """Delete a contract."""
        try:
            contract = self.get_contract_by_id(contract_id)
            if not contract:
                raise Exception("Contract not found")

            self.session.delete(contract)
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise Exception(f"Contract deletion failed: {e.orig.diag.message_detail}")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error deleting contract: {e}")

    def get_unsigned_contracts(self, commercial_id):
        """Retrieve all unsigned contracts for a specific commercial."""
        try:
            return (
                self.session.query(Contract)
                .filter(
                    Contract.signed == False,
                    Contract.client.has(
                        commercial_contact=commercial_id
                    ),  # Filtrer par commercial
                )
                .all()
            )
        except Exception as e:
            raise Exception(f"Error retrieving unsigned contracts: {e}")

    def get_unpaid_contracts(self, commercial_id):
        """Retrieve all unpaid contracts for a specific commercial."""
        try:
            return (
                self.session.query(Contract)
                .filter(
                    Contract.amount_remaining > 0,
                    Contract.client.has(
                        commercial_contact=commercial_id
                    ),  # Filtrer par commercial
                )
                .all()
            )
        except Exception as e:
            raise Exception(f"Error retrieving unpaid contracts: {e}")

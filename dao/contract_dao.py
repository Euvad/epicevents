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

    def get_contract_by_id(self, contract_id: int) -> Contract:
        """Retrieve a contract by its ID."""
        contract = (
            self.session.query(Contract).filter(Contract.id == contract_id).first()
        )
        if not contract:
            raise Exception("Contract not found")
        return contract

    def get_all_contracts(self) -> list[Contract]:
        """Retrieve all contracts."""
        return self.session.query(Contract).all()

    def update_contract(self, contract: Contract):
        """Update an existing contract's details."""
        existing_contract = self.get_contract_by_id(contract.id)
        if existing_contract:
            existing_contract.total_amount = contract.total_amount
            existing_contract.amount_remaining = contract.amount_remaining
            existing_contract.signed = contract.signed
            try:
                self.session.commit()
                return existing_contract
            except IntegrityError as e:
                self.session.rollback()
                raise Exception(f"Contract update failed: {e.orig.diag.message_detail}")

    def delete_contract(self, contract_id: int):
        """Delete a contract."""
        contract = self.get_contract_by_id(contract_id)
        if contract:
            try:
                self.session.delete(contract)
                self.session.commit()
            except IntegrityError as e:
                self.session.rollback()
                raise Exception(
                    f"Contract deletion failed: {e.orig.diag.message_detail}"
                )

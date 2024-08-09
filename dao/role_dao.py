# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    role_dao.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: Vadim <euvad.public@proton.me>             +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/08/07 15:24:07 by Vadim             #+#    #+#              #
#    Updated: 2024/08/09 12:55:10 by Vadim            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from sqlalchemy.orm import Session
from models.role import Role


class RoleDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_role(self, name, permissions):
        """Create a new role with specified permissions."""
        role = Role(name=name, permissions=permissions)
        self.session.add(role)
        self.session.commit()
        return role

    def get_role_by_name(self, name) -> Role:
        """Retrieve a role by its name."""
        return self.session.query(Role).filter(Role.name == name).first()

    def get_all_roles(self) -> list[Role]:
        """Retrieve all roles."""
        return self.session.query(Role).all()

    def update_role(self, role: Role):
        """Update an existing role."""
        existing_role = self.session.query(Role).filter(Role.id == role.id).first()
        if existing_role:
            existing_role.name = role.name
            existing_role.permissions = role.permissions
            self.session.commit()
            return existing_role
        return None

    def delete_role(self, role: Role):
        """Delete an existing role."""
        self.session.delete(role)
        self.session.commit()

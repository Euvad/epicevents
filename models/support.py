from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

# Support Model
class Support(Base):
    __tablename__ = 'support'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    support_user_id = Column(Integer, ForeignKey('users.id'))  # Si un utilisateur est assigné

    client = relationship('Client', back_populates='supports')
    contract = relationship('Contract')
    support_user = relationship('User')  # Relation optionnelle avec User

    def __repr__(self):
        return (f"<Support(support_user_id={self.support_user_id}, client_id={self.client_id}, "
                f"contract_id={self.contract_id})>")

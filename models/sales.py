from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


# Sales Model
class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    sales_name = Column(String, nullable=False)

    client = relationship("Client", back_populates="sales")

    def __repr__(self):
        return f"<Sales(sales_name={self.sales_name}, client_id={self.client_id})>"

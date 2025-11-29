from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    is_paid = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    users = relationship("User", back_populates="role")

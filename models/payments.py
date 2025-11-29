from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="UZS")
    screenshot = Column(String, nullable=True)  # file path or telegram file_id
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")

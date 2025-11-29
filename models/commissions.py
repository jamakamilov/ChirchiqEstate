from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True)
    percent = Column(Float, default=2.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# table for commission requests
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
class CommissionRequest(Base):
    __tablename__ = "commission_requests"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=True)
    sale_amount = Column(Float, nullable=False)
    commission_amount = Column(Float, nullable=False)
    screenshot = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
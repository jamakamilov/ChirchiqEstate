from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Commission(Base):
    __tablename__ = "commissions"

    id = Column(Integer, primary_key=True)
    percent = Column(Float, default=2.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

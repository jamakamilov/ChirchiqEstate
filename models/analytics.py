from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class ViewStat(Base):
    __tablename__ = "view_stats"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=True)  # view, save, contact
    created_at = Column(DateTime(timezone=True), server_default=func.now())

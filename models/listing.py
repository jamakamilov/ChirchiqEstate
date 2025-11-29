from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.sql import func

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=True)
    category = Column(String, nullable=False)  # e.g., apartment, house, land
    deal_type = Column(String, nullable=False)  # sale, rent
    region = Column(String, nullable=True)
    district = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    currency = Column(String, default="UZS")
    area = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    floors_total = Column(Integer, nullable=True)
    rooms = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    coords = Column(JSON, nullable=True)  # {"lat":..., "lon":...}
    photos = Column(JSON, nullable=True)  # list of file_ids or paths
    status = Column(String, default="draft")  # draft, moderation, published, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    published_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User")

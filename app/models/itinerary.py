import uuid
from sqlalchemy import Column, String, DateTime, Date, Integer, Uuid, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Itinerary(Base):
    __tablename__ = "itineraries"

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    trip_uuid = Column(Uuid, ForeignKey("trips.uuid"), nullable=False)
    day_number = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    trip = relationship("Trip", back_populates="itineraries")

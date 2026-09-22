import uuid
from sqlalchemy import Column, String, DateTime, Date, Uuid, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Trip(Base):
    __tablename__ = "trips"

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_uuid = Column(Uuid, ForeignKey("users.uuid"), nullable=False)
    title = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="trips")
    itineraries = relationship("Itinerary", back_populates="trip")
    places = relationship("TripPlace", back_populates="trip")

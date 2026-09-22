import uuid
from sqlalchemy import Column, String, Integer, Uuid, ForeignKey, Time
from sqlalchemy.orm import relationship
from app.core.database import Base

class TripPlace(Base):
    __tablename__ = "trip_places"

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    trip_uuid = Column(Uuid, ForeignKey("trips.uuid"), nullable=False)
    place_uuid = Column(Uuid, ForeignKey("places.uuid"), nullable=False)
    day_number = Column(Integer, nullable=True)
    visit_time = Column(Time, nullable=True)
    notes = Column(String, nullable=True)

    trip = relationship("Trip", back_populates="places")
    place = relationship("Place", back_populates="trips")

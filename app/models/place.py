import uuid
from sqlalchemy import Column, String, Float, Uuid
from sqlalchemy.orm import relationship
from app.core.database import Base

class Place(Base):
    __tablename__ = "places"

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    address = Column(String, nullable=True)
    rating = Column(Float, nullable=True)
    description = Column(String, nullable=True)
    external_place_id = Column(String, nullable=True, unique=True)

    trips = relationship("TripPlace", back_populates="place")

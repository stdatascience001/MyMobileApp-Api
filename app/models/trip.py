from uuid import UUID, uuid4
import sqlalchemy
import datetime
from sqlalchemy import String, DateTime, Date, Uuid, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, Dict, Any
from app.core.database import Base

class Trip(Base):
    __tablename__ = "trips"

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4, index=True)
    user_uuid: Mapped[UUID] = mapped_column(Uuid, ForeignKey("users.uuid"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    destination: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    preferences: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    itinerary_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    is_generated: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="trips")
    itineraries = relationship("Itinerary", back_populates="trip", cascade="all, delete-orphan")
    places = relationship("TripPlace", back_populates="trip", cascade="all, delete-orphan")

import uuid
from sqlalchemy import Column, String, DateTime, Uuid
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    uuid = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    trips = relationship("Trip", back_populates="user")

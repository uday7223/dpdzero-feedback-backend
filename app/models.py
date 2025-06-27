from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, DateTime, Boolean
from app.database import Base
import enum
from sqlalchemy.orm import relationship
from datetime import datetime

class RoleEnum(enum.Enum):
    manager = "manager"
    employee = "employee"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # NEW
    manager = relationship("User", remote_side=[id], backref="employees")

class SentimentEnum(enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    strengths = Column(Text, nullable=False)
    areas_to_improve = Column(Text, nullable=False)
    sentiment = Column(Enum(SentimentEnum), nullable=False)

    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    manager = relationship("User", foreign_keys=[manager_id], backref="feedback_given")
    employee = relationship("User", foreign_keys=[employee_id], backref="feedback_received")

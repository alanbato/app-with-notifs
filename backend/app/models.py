from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, mapped_column

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username: Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name: Column(String)
    hashed_password = Column(String)
    notifications = relationship("Association")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)


class UserNotification(Base):
    __tablename__ = "user_notifications"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    notification_id = mapped_column(ForeignKey("notifications.id"), primary_key=True)
    read = Column(Boolean)
    notification = relationship("Notification")

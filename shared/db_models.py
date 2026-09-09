from shared.db import Base
from sqlalchemy import (
    Column, Integer, String, DateTime, Boolean, JSON, 
    ForeignKey, func, UniqueConstraint
)
from sqlalchemy.orm import relationship


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
    api_key = Column(String(255), nullable=False, unique=True, index=True) 
    
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    templates = relationship("NotificationTemplate", back_populates="application")
    notifications = relationship("Notification", back_populates="application")


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    
    code = Column(String(100), nullable=False) 
    subject = Column(String(255), nullable=True) 
    template_path = Column(String(255), nullable=False)

    sender_name = Column(String(100), nullable=True) 
    sender_email = Column(String(255), nullable=True) 
    reply_to = Column(String(255), nullable=True)     
    
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    application = relationship("Application", back_populates="templates")
    notifications = relationship("Notification", back_populates="template")

    __table_args__ = (
        UniqueConstraint('application_id', 'code', name='_app_template_uc'),
    )


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, index=True)
    
    template_id = Column(Integer, ForeignKey("notification_templates.id"), nullable=False, index=True)

    idempotency_key = Column(String(255), nullable=False, unique=True, index=True)
    recipient = Column(String(255), nullable=False, index=True)
    channel = Column(String(20), nullable=False, default="EMAIL") # EMAIL, SMS, PUSH
    
    payload = Column(JSON, nullable=False)
    
    status = Column(String(20), nullable=False, default="PENDING", index=True) # PENDING, SENT, FAILED
    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)
    error_message = Column(String(500), nullable=True) 
    
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    application = relationship("Application", back_populates="notifications")
    template = relationship("NotificationTemplate", back_populates="notifications")
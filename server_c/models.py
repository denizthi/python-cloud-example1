# app/models.py
import uuid

from sqlalchemy import Column, String, Text, UniqueConstraint, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class Account(Base):
    __tablename__ = "accounts"
    
    __table_args__ = (
        UniqueConstraint("email", name="accounts_email_key"),)

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String(50), nullable=False)
    password_hash = Column(Text, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)



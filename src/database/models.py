## Description: Database models for the application.

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

import datetime

from typing import List

class Base(DeclarativeBase):
    pass

class Feedback(Base):
    """
    Feedback model.
    """
    __tablename__ = "feedback"

    feedback_id: Mapped[str] = mapped_column(String, primary_key=True)
    feedback_raw: Mapped[str] = mapped_column(String)
    feedback_sentiment: Mapped[str] = mapped_column(String)
    feedback_created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    feedback_requested_features: Mapped[List["RequestedFeature"]] = relationship(
        "RequestedFeature",
        back_populates="feedback",
    )

    def __repr__(self) -> str:
        return f"Feedbacks:(id:'{self.feedback_id}', feedback:'{self.feedback_raw}', sentiment:'{self.feedback_sentiment}', features:'{self.feedback_requested_features}', create_at:{self.feedback_created_at})"
    
class RequestedFeature(Base):
    """
    Requested Feature model.
    """
    __tablename__ = "requested_feature"

    requested_feature_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    requested_feature_code: Mapped[str] = mapped_column(String)
    requested_feature_reason: Mapped[str] = mapped_column(String)
    feedback_id: Mapped[String] = mapped_column(
        String,
        ForeignKey("feedback.feedback_id"),
    )
    feedback: Mapped[Feedback] = relationship(
        "Feedback",
        back_populates="feedback_requested_features",
    )

    def __repr__(self) -> str:
        return f"RequestedFeature:(id:'{self.requested_feature_id}', code:'{self.requested_feature_code}', reason:'{self.requested_feature_reason}')"

class Email(Base):
    """
    Email model.
    """
    __tablename__ = "email"

    email_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email_email: Mapped[str] = mapped_column(String, unique=True)
    email_name: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Email:(email:'{self.email_email}', name:'{self.email_name}')"

from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.document import Document


class DocumentAnalysis(Base):
    __tablename__ = "document_analyses"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    model_name: Mapped[str]= mapped_column(
        String(100),
        nullable=False,
    )

    analysis: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    created_at: Mapped[datetime]= mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="analysis",
    )
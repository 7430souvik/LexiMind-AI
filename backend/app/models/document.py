from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.document_analysis import DocumentAnalysis
    from app.models.document_chunk import DocumentChunk


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="uploaded",
        nullable=False,
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # =========================
    # Relationships
    # =========================

    owner: Mapped["User"] = relationship(
        "User",
        back_populates="documents",
    )

    analysis: Mapped["DocumentAnalysis"] = relationship(
        "DocumentAnalysis",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )
    
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
import uuid

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy Models in Wynthora.
    """
    pass

class AuditMixin:
    """
    Mixin to track dataset versioning and audit trails for all tables.
    """
    # Metadata for Lineage and Versioning
    dataset_version: Mapped[str] = mapped_column(nullable=True)
    schema_version: Mapped[str] = mapped_column(nullable=True, default="1.0")
    source_version: Mapped[str] = mapped_column(nullable=True)
    checksum: Mapped[str] = mapped_column(nullable=True)
    
    # Timestamps
    retrieved_at: Mapped[datetime] = mapped_column(nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
    
    record_version: Mapped[int] = mapped_column(default=1)

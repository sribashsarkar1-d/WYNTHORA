import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Index, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class GlobalEventModel(Base):
    """
    SQLAlchemy model for tracking global events.
    """
    __tablename__ = "global_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    severity = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True) # Soft delete
    
    __table_args__ = (
        Index('idx_global_events_category', 'category'),
        Index('idx_global_events_active', 'active'),
    )

class CountryModel(Base):
    """
    SQLAlchemy model for country data.
    """
    __tablename__ = "countries"

    iso_code = Column(String(3), primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    region = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class EconomicTimeSeriesModel(Base):
    """
    SQLAlchemy model for historical economic data (GDP, Inflation, etc.)
    """
    __tablename__ = "economic_time_series"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code = Column(String(3), ForeignKey("countries.iso_code", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    gdp_usd = Column(Numeric(20, 2), nullable=True)
    inflation_rate = Column(Numeric(5, 2), nullable=True)
    unemployment_rate = Column(Numeric(5, 2), nullable=True)
    version = Column(Integer, default=1, nullable=False) # Optimistic locking
    created_at = Column(DateTime, default=datetime.utcnow)
    
    country = relationship("CountryModel", backref="economic_data")
    
    __table_args__ = (
        Index('idx_economic_country_year', 'country_code', 'year', unique=True),
    )

from sqlalchemy import String, Text, Boolean, ForeignKey, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class ServiceCategory(Base, TimestampMixin):
    """e.g. Digital Products, Applications, Infrastructure, Business Solutions."""

    __tablename__ = "service_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    icon: Mapped[str | None] = mapped_column(String(100))
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    services: Mapped[list["Service"]] = relationship(back_populates="category")


class Service(Base, TimestampMixin):
    """e.g. Website Development, E-Commerce, CRM, Hosting."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("service_categories.id", ondelete="RESTRICT"))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(170), unique=True, nullable=False, index=True)
    short_description: Mapped[str | None] = mapped_column(String(300))
    long_description: Mapped[str | None] = mapped_column(Text)
    starting_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    is_custom_quote_only: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

    # SEO
    meta_title: Mapped[str | None] = mapped_column(String(200))
    meta_description: Mapped[str | None] = mapped_column(String(300))

    category: Mapped["ServiceCategory"] = relationship(back_populates="services")
    packages: Mapped[list["ServicePackage"]] = relationship(back_populates="service", cascade="all, delete-orphan")
    features: Mapped[list["ServiceFeature"]] = relationship(back_populates="service", cascade="all, delete-orphan")
    technologies: Mapped[list["Technology"]] = relationship(
        secondary="service_technologies", back_populates="services"
    )


class ServicePackage(Base, TimestampMixin):
    """e.g. Starter / Business / Professional / Enterprise for a given service."""

    __tablename__ = "service_packages"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # Starter, Business, Professional, Enterprise
    price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    is_custom_quote: Mapped[bool] = mapped_column(Boolean, default=False)
    billing_interval: Mapped[str] = mapped_column(String(20), default="one_time")  # one_time | monthly | yearly
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

    service: Mapped["Service"] = relationship(back_populates="packages")


class ServiceFeature(Base, TimestampMixin):
    __tablename__ = "service_features"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0)

    service: Mapped["Service"] = relationship(back_populates="features")


class Technology(Base, TimestampMixin):
    """Tech stack badges shown on service/project cards (React, FastAPI, MySQL...)."""

    __tablename__ = "technologies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    icon: Mapped[str | None] = mapped_column(String(100))

    services: Mapped[list["Service"]] = relationship(secondary="service_technologies", back_populates="technologies")


class ServiceTechnology(Base):
    """Association: services <-> technologies."""

    __tablename__ = "service_technologies"

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), primary_key=True)
    technology_id: Mapped[int] = mapped_column(ForeignKey("technologies.id", ondelete="CASCADE"), primary_key=True)

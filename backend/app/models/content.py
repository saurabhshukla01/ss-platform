from sqlalchemy import String, Text, Boolean, ForeignKey, DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.mixins import TimestampMixin


class Page(Base, TimestampMixin):
    """Top-level static page (About, FAQ/Legal, Contact) with admin-editable sections."""

    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(150), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)

    sections: Mapped[list["PageSection"]] = relationship(back_populates="page", cascade="all, delete-orphan")


class PageSection(Base, TimestampMixin):
    """A reorderable content block within a page (hero, why-choose-us, testimonials, FAQ, etc.)."""

    __tablename__ = "page_sections"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"))
    section_type: Mapped[str] = mapped_column(String(60), nullable=False)  # hero | stats | why_us | cta | ...
    content_json: Mapped[dict | None] = mapped_column(JSON)  # flexible admin-editable content
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    page: Mapped["Page"] = relationship(back_populates="sections")


class Banner(Base, TimestampMixin):
    __tablename__ = "banners"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500))
    link_url: Mapped[str | None] = mapped_column(String(500))
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    starts_at: Mapped[DateTime | None] = mapped_column(DateTime)
    ends_at: Mapped[DateTime | None] = mapped_column(DateTime)


class Announcement(Base, TimestampMixin):
    """Animated announcement/breaking-news bar content."""

    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(300), nullable=False)
    link_url: Mapped[str | None] = mapped_column(String(500))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    starts_at: Mapped[DateTime | None] = mapped_column(DateTime)
    ends_at: Mapped[DateTime | None] = mapped_column(DateTime)


class Offer(Base, TimestampMixin):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    service_id: Mapped[int | None] = mapped_column(ForeignKey("services.id", ondelete="SET NULL"))
    discount_label: Mapped[str | None] = mapped_column(String(100))  # e.g. "20% OFF"
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    starts_at: Mapped[DateTime | None] = mapped_column(DateTime)
    ends_at: Mapped[DateTime | None] = mapped_column(DateTime)


class BlogCategory(Base, TimestampMixin):
    __tablename__ = "blog_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(140), unique=True, nullable=False)

    blogs: Mapped[list["Blog"]] = relationship(back_populates="category")


class Blog(Base, TimestampMixin):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("blog_categories.id", ondelete="SET NULL"))
    admin_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id", ondelete="SET NULL"))
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    slug: Mapped[str] = mapped_column(String(270), unique=True, nullable=False, index=True)
    excerpt: Mapped[str | None] = mapped_column(String(400))
    content: Mapped[str | None] = mapped_column(Text)
    cover_image_url: Mapped[str | None] = mapped_column(String(500))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[DateTime | None] = mapped_column(DateTime)

    # SEO
    meta_title: Mapped[str | None] = mapped_column(String(200))
    meta_description: Mapped[str | None] = mapped_column(String(300))

    category: Mapped["BlogCategory | None"] = relationship(back_populates="blogs")
    tags: Mapped[list["BlogTag"]] = relationship(secondary="blog_tag_map", back_populates="blogs")


class BlogTag(Base, TimestampMixin):
    __tablename__ = "blog_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    blogs: Mapped[list["Blog"]] = relationship(secondary="blog_tag_map", back_populates="tags")


class BlogTagMap(Base):
    __tablename__ = "blog_tag_map"

    blog_id: Mapped[int] = mapped_column(ForeignKey("blogs.id", ondelete="CASCADE"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("blog_tags.id", ondelete="CASCADE"), primary_key=True)


class Faq(Base, TimestampMixin):
    __tablename__ = "faqs"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(300), nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    service_id: Mapped[int | None] = mapped_column(ForeignKey("services.id", ondelete="SET NULL"))
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

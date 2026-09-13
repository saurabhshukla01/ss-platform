"""
Import every model module here so that Base.metadata is fully populated
for Alembic autogenerate and for `Base.metadata.create_all()` in dev/testing.
"""

from app.models import identity      # users, admins, roles, permissions
from app.models import services      # service_categories, services, packages, features, technologies
from app.models import crm           # customers, inquiries, leads, lead_notes, lead_followups, lead_status_history
from app.models import commerce      # orders, payments, payment_transactions, invoices, coupons
from app.models import subscriptions # subscription_plans, subscriptions, subscription_items, wallets, tokens
from app.models import analytics     # visitors, visitor_sessions, page_views, analytics_events
from app.models import content       # pages, page_sections, banners, announcements, offers, blogs, faqs
from app.models import brand         # projects, team_members, testimonials, social_links, settings
from app.models import operations    # notifications, communication_logs, audit_logs, seo_meta, redirects

__all__ = [
    "identity", "services", "crm", "commerce", "subscriptions",
    "analytics", "content", "brand", "operations",
]

"""
SS PLATFORM DATABASE SEEDER
===========================

Run from backend directory:

    python -m app.seed

Purpose:
- Creates missing SQLAlchemy tables.
- Inserts master data first.
- Stores generated/existing IDs in REF.
- Inserts mapping/relationship data only after master data exists.
- Seeds meaningful demo/business data.
- Safe to run repeatedly.
- Never deletes existing records.
- Uses one database transaction.
- Rolls back the complete seed if any step fails.
- Does not touch alembic_version.

Demo admin:
    Email:    admin@ssplatform.com
    Password: Admin@123456

Database:
    Uses app.core.database.engine
    which must use settings.DATABASE_URL.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from sqlalchemy import MetaData, Table, inspect, select

from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password

# Register every SQLAlchemy model.
import app.models  # noqa: F401


# ============================================================================
# CONFIGURATION
# ============================================================================

ADMIN_EMAIL = "admin@ssplatform.com"
ADMIN_PASSWORD = "Admin@123456"

DEMO_DOMAIN = "https://ssplatform.com"

# All inserted/existing master IDs are stored here.
#
# Example:
#
# REF["service"]["crm"] = 7
# REF["technology"]["React"] = 2
# REF["customer"]["customer1@example.com"] = 4
#
REF: dict[str, dict[Any, Any]] = {}


# ============================================================================
# DEMO MASTER DATA
# ============================================================================

PERMISSION_ROWS = [
    ("services.manage", "Manage services and service content"),
    ("crm.view", "View CRM data"),
    ("crm.manage", "Manage customers, inquiries and leads"),
    ("analytics.view", "View visitor and analytics data"),
    ("payments.manage", "Manage payments and transactions"),
    ("subscriptions.manage", "Manage subscriptions and plans"),
    ("content.manage", "Manage website content"),
    ("settings.manage", "Manage platform settings"),
    ("users.manage", "Manage users and admins"),
    ("blogs.manage", "Manage blog content"),
    ("offers.manage", "Manage offers and coupons"),
    ("orders.manage", "Manage orders and invoices"),
    ("notifications.manage", "Manage notifications"),
]


ROLE_ROWS = [
    (
        "SUPER_ADMIN",
        "Full access to SS Platform",
    ),
    (
        "CONTENT_MANAGER",
        "Website and blog content management",
    ),
    (
        "SALES_MANAGER",
        "CRM, leads and order management",
    ),
]


CATEGORY_ROWS = [
    (
        "Digital Products",
        "digital-products",
        "Website development, e-commerce, admin panels and APIs",
        "globe",
        1,
        True,
    ),
    (
        "Applications",
        "applications",
        "Mobile applications, CRM, HRMS and custom software",
        "layers",
        2,
        True,
    ),
    (
        "Infrastructure",
        "infrastructure",
        "Hosting, deployment, SSL, DNS and maintenance",
        "server",
        3,
        True,
    ),
    (
        "Business Solutions",
        "business-solutions",
        "Automation, integration, reporting and custom platforms",
        "briefcase",
        4,
        True,
    ),
]


SERVICE_ROWS = [
    (
        "digital-products",
        "Website Development",
        "website-development",
        "Fast responsive business websites with an admin panel.",
        "React frontend, FastAPI backend and MySQL database.",
        Decimal("15000"),
        False,
        1,
    ),
    (
        "digital-products",
        "E-Commerce",
        "e-commerce",
        "Complete online store with catalogue, checkout and order management.",
        "Product catalogue, cart, checkout, payments, inventory and admin tools.",
        Decimal("35000"),
        False,
        2,
    ),
    (
        "digital-products",
        "Admin Panel",
        "admin-panel",
        "Secure administration dashboard for business operations.",
        "Role-based access, dashboards, content, CRM and reporting.",
        Decimal("20000"),
        False,
        3,
    ),
    (
        "digital-products",
        "REST API",
        "rest-api",
        "Production-ready REST API development.",
        "FastAPI, JWT authentication, validation, Swagger and MySQL.",
        Decimal("18000"),
        False,
        4,
    ),
    (
        "applications",
        "Mobile Application",
        "mobile-application",
        "Android/iOS application connected to a business API.",
        "Customer apps, business apps, authentication, notifications and API integration.",
        None,
        True,
        1,
    ),
    (
        "applications",
        "CRM",
        "crm",
        "Lead and customer management platform.",
        "Inquiry capture, pipeline, follow-ups, notes and communication history.",
        Decimal("25000"),
        False,
        2,
    ),
    (
        "infrastructure",
        "Hosting & Deployment",
        "hosting-deployment",
        "Hosting and deployment setup for web applications.",
        "Linux, Nginx, SSL, DNS, deployment and maintenance.",
        Decimal("5000"),
        False,
        1,
    ),
    (
        "business-solutions",
        "Automation & Integration",
        "automation-integration",
        "Business workflow automation and third-party integrations.",
        "API integrations, scheduled jobs, notifications and reporting.",
        None,
        True,
        1,
    ),
]


TECHNOLOGY_ROWS = [
    ("React", "react"),
    ("FastAPI", "python"),
    ("Python", "python"),
    ("Laravel", "php"),
    ("PHP", "php"),
    ("MySQL", "database"),
    ("Node.js", "node"),
    ("JavaScript", "javascript"),
    ("AWS", "cloud"),
    ("Docker", "docker"),
    ("Nginx", "server"),
    ("Linux", "server"),
    ("Git", "git"),
]


PAGE_ROWS = [
    ("home", "Home", True),
    ("about", "About SS Platform", True),
    ("services", "Services", True),
    ("pricing", "Pricing", True),
    ("contact", "Contact", True),
    ("blog", "Blog", True),
]


BLOG_CATEGORY_ROWS = [
    ("Web Development", "web-development"),
    ("E-Commerce", "e-commerce"),
    ("Business Automation", "business-automation"),
    ("Technology", "technology"),
]


BLOG_TAG_ROWS = [
    "React",
    "FastAPI",
    "Python",
    "Laravel",
    "MySQL",
    "E-Commerce",
    "REST API",
    "CRM",
    "Cloud",
    "Automation",
    "Admin Panel",
]


SOCIAL_ROWS = [
    ("Instagram", "https://instagram.com/ssservice", True),
    ("Facebook", "https://facebook.com/ssservice", True),
    ("YouTube", "https://youtube.com/@ssservice", True),
    ("LinkedIn", "https://linkedin.com/company/ssservice", True),
]


REDIRECT_ROWS = [
    ("/home", "/", 301, True),
    ("/web-development", "/services/website-development", 301, True),
    ("/api", "/services/rest-api", 301, True),
]


BANNER_ROWS = [
    (
        "Build. Automate. Grow.",
        "/assets/img/banner-1.jpg",
        "/services",
        1,
        True,
    ),
    (
        "Website + Backend Development",
        "/assets/img/banner-2.jpg",
        "/services",
        2,
        True,
    ),
    (
        "React + FastAPI + MySQL Solutions",
        "/assets/img/banner-3.jpg",
        "/services",
        3,
        True,
    ),
]


ANNOUNCEMENT_ROWS = [
    (
        "Launch offer: Complete website with frontend and backend from ₹19,999.",
        "/services",
        True,
    ),
    (
        "Business websites include responsive UI, API integration and admin support.",
        "/services",
        True,
    ),
    (
        "New: 30-day maintenance window available with selected business plans.",
        "/pricing",
        True,
    ),
]


PROJECT_ROWS = [
    (
        "SS Collections Catalogue Platform",
        "ss-collections-catalogue-platform",
        "Dynamic product catalogue with admin-managed pricing and content.",
        "React, FastAPI, MySQL",
        "live",
        True,
    ),
    (
        "Client CRM Rollout",
        "client-crm-rollout",
        "Lead pipeline and follow-up tracking for service businesses.",
        "React, FastAPI, JWT",
        "completed",
        True,
    ),
    (
        "Hosting & Maintenance Program",
        "hosting-maintenance-program",
        "Managed hosting, SSL renewal and uptime monitoring.",
        "Nginx, Linux, Cloudflare",
        "live",
        False,
    ),
]


TESTIMONIAL_ROWS = [
    (
        "Retail Client",
        "SS Collections Group",
        "The admin panel makes it easy to update products, prices and offers.",
        5,
    ),
    (
        "Service Business Owner",
        "Local Business",
        "Inquiries now move directly into a structured sales pipeline.",
        5,
    ),
    (
        "Startup Founder",
        "Demo Technologies Pvt Ltd",
        "The API and dashboard reduced manual business operations.",
        4,
    ),
]


SETTING_ROWS = [
    (
        "theme",
        "site_name",
        "Saurabh Shukla Technology Platform",
        False,
    ),
    (
        "theme",
        "tagline",
        "Build. Automate. Grow.",
        False,
    ),
    (
        "theme",
        "primary_color",
        "#000000",
        False,
    ),
    (
        "theme",
        "primary_dark_color",
        "#111111",
        False,
    ),
    (
        "theme",
        "accent_color",
        "#FFFFFF",
        False,
    ),
    (
        "site",
        "domain",
        DEMO_DOMAIN,
        False,
    ),
    (
        "site",
        "support_email",
        ADMIN_EMAIL,
        False,
    ),
    (
        "site",
        "currency",
        "INR",
        False,
    ),
    (
        "site",
        "delivery_note",
        "Demo services are delivered according to project scope.",
        False,
    ),
]


USER_ROWS = [
    (
        "Demo Customer One",
        "customer1@example.com",
        "+919999000101",
    ),
    (
        "Demo Customer Two",
        "customer2@example.com",
        "+919999000102",
    ),
    (
        "Demo Business Owner",
        "owner@example.com",
        "+919999000103",
    ),
    (
        "Demo Startup Founder",
        "founder@example.com",
        "+919999000104",
    ),
]


CUSTOMER_ROWS = [
    (
        "Demo Customer One",
        "customer1@example.com",
        "+919999000101",
        "Demo Retail Pvt Ltd",
    ),
    (
        "Demo Customer Two",
        "customer2@example.com",
        "+919999000102",
        "Demo Solutions Pvt Ltd",
    ),
    (
        "Demo Business Owner",
        "owner@example.com",
        "+919999000103",
        "Local Business",
    ),
    (
        "Demo Startup Founder",
        "founder@example.com",
        "+919999000104",
        "Demo Startup",
    ),
]


# ============================================================================
# HELPERS
# ============================================================================

def utcnow() -> datetime:
    """
    Return current UTC datetime.

    Kept as a helper so all seeded timestamps use the same style.
    """
    return datetime.utcnow()


def new_uuid() -> str:
    """
    Generate a UUID string.

    Kept available for future seed records.
    """
    return str(uuid.uuid4())


def reflect_all() -> MetaData:
    """
    Reflect the actual database schema.

    This lets the seeder work against the real database rather than
    assuming the model definitions and database are perfectly identical.
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata


def table(metadata: MetaData, name: str) -> Table:
    """
    Return a reflected table or raise a clear error.
    """
    if name not in metadata.tables:
        raise RuntimeError(
            f"Required database table '{name}' does not exist."
        )

    return metadata.tables[name]


def pk_name(t: Table) -> str:
    """
    Return the first primary-key column name.
    """
    columns = list(t.primary_key.columns)

    if not columns:
        raise RuntimeError(
            f"Table '{t.name}' does not have a primary key."
        )

    return columns[0].name


def resolve(value: Any) -> Any:
    """
    Resolve a deferred reference.

    Example:

        ref("service", "crm")

    becomes:

        actual service primary-key value
    """

    if (
        isinstance(value, tuple)
        and len(value) == 2
        and value[0] == "$ref"
    ):
        return value[1]

    return value


def ref(kind: str, key: Any) -> tuple[str, Any]:
    """
    Return a deferred reference from REF.

    This intentionally fails loudly if a parent/master record has
    not already been seeded.
    """

    try:
        return ("$ref", REF[kind][key])

    except KeyError as exc:

        available = sorted(
            str(value)
            for value in REF.get(kind, {}).keys()
        )

        raise RuntimeError(
            f"Missing seed reference: {kind}={key!r}. "
            f"Available keys: {available}"
        ) from exc


def existing_row(
    db,
    t: Table,
    where: dict[str, Any],
):
    """
    Find the first matching row.

    Only columns actually present in the reflected database table
    are used.
    """

    conditions = []

    for key, value in where.items():

        if key not in t.c:
            continue

        value = resolve(value)

        if value is None:
            conditions.append(
                t.c[key].is_(None)
            )
        else:
            conditions.append(
                t.c[key] == value
            )

    stmt = select(t)

    if conditions:
        stmt = stmt.where(*conditions)

    stmt = stmt.limit(1)

    return (
        db.execute(stmt)
        .mappings()
        .first()
    )


def clean_values(
    t: Table,
    values: dict[str, Any],
) -> dict[str, Any]:
    """
    Keep only database columns.

    None values are omitted so database defaults can apply.
    """

    clean: dict[str, Any] = {}

    for key, value in values.items():

        if key not in t.c:
            continue

        value = resolve(value)

        if value is None:
            continue

        clean[key] = value

    return clean


def insert_or_get(
    db,
    metadata: MetaData,
    table_name: str,
    values: dict[str, Any],
    lookup: dict[str, Any],
):
    """
    Insert one row if it does not already exist.

    Existing records are reused.

    Returns:
        (row_dict, created_bool)
    """

    t = table(
        metadata,
        table_name,
    )

    lookup_clean = {
        key: resolve(value)
        for key, value in lookup.items()
        if key in t.c
    }

    if not lookup_clean:
        raise RuntimeError(
            f"No valid lookup columns supplied "
            f"for table '{table_name}'."
        )

    existing = existing_row(
        db,
        t,
        lookup_clean,
    )

    if existing:
        return dict(existing), False

    clean = clean_values(
        t,
        values,
    )

    if not clean:
        raise RuntimeError(
            f"No valid insert columns supplied "
            f"for table '{table_name}'."
        )

    result = db.execute(
        t.insert().values(**clean)
    )

    db.flush()

    inserted_pk = None

    if result.inserted_primary_key:
        inserted_pk = result.inserted_primary_key[0]

    row = None

    if inserted_pk is not None:

        pk = pk_name(t)

        row = (
            db.execute(
                select(t).where(
                    t.c[pk] == inserted_pk
                )
            )
            .mappings()
            .first()
        )

    if row is None:

        row = existing_row(
            db,
            t,
            lookup_clean,
        )

    if row is None:
        raise RuntimeError(
            f"Unable to fetch inserted row "
            f"from '{table_name}'."
        )

    return dict(row), True


def save_ref(
    kind: str,
    key: Any,
    row: dict[str, Any],
    t: Table,
):
    """
    Save a master record's primary key into REF.
    """

    REF.setdefault(
        kind,
        {},
    )[key] = row[pk_name(t)]


def require_tables(
    md: MetaData,
    table_names: list[str],
):
    """
    Verify required tables exist.
    """

    missing = [
        name
        for name in table_names
        if name not in md.tables
    ]

    if missing:

        raise RuntimeError(
            "Database schema is missing required tables:\n  - "
            + "\n  - ".join(sorted(missing))
        )


def print_step(title: str):
    """
    Print a consistent seeder section header.
    """

    print("\n" + "=" * 75)
    print(title)
    print("=" * 75)


def assert_ref(
    kind: str,
    key: Any,
):
    """
    Explicitly verify that a required REF exists.

    This makes mapping failures easier to understand.
    """

    if kind not in REF:
        raise RuntimeError(
            f"Required seed reference group '{kind}' "
            f"has not been created."
        )

    if key not in REF[kind]:
        raise RuntimeError(
            f"Required seed reference '{kind}={key}' "
            f"has not been created."
        )


# ============================================================================
# STEP 1 — PERMISSIONS MASTER
# ============================================================================

def seed_permissions(db, md):

    print_step("[1] MASTER: Permissions")

    permission_t = table(
        md,
        "permissions",
    )

    for code, description in PERMISSION_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "permissions",
            {
                "code": code,
                "description": description,
            },
            {
                "code": code,
            },
        )

        save_ref(
            "permission",
            code,
            row,
            permission_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"permission: {code}"
        )


# ============================================================================
# STEP 2 — ROLES MASTER
# ============================================================================

def seed_roles(db, md):

    print_step("[2] MASTER: Roles")

    role_t = table(
        md,
        "roles",
    )

    for name, description in ROLE_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "roles",
            {
                "name": name,
                "description": description,
            },
            {
                "name": name,
            },
        )

        save_ref(
            "role",
            name,
            row,
            role_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"role: {name}"
        )


# ============================================================================
# STEP 3 — ADMIN MASTER
# ============================================================================

def seed_admin(db, md):

    print_step("[3] MASTER: Admin")

    assert_ref(
        "role",
        "SUPER_ADMIN",
    )

    admin_t = table(
        md,
        "admins",
    )

    admin, created = insert_or_get(
        db,
        md,
        "admins",
        {
            "full_name": "Saurabh Shukla",
            "email": ADMIN_EMAIL,
            "hashed_password": hash_password(
                ADMIN_PASSWORD
            ),
            "is_active": True,
            "is_super_admin": True,
            "role_id": ref(
                "role",
                "SUPER_ADMIN",
            ),
        },
        {
            "email": ADMIN_EMAIL,
        },
    )

    save_ref(
        "admin",
        ADMIN_EMAIL,
        admin,
        admin_t,
    )

    print(
        f"  {'CREATED' if created else 'EXISTS '} "
        f"admin: {ADMIN_EMAIL}"
    )


# ============================================================================
# STEP 4 — ROLE/PERMISSION MAPPING
# ============================================================================

def seed_role_permissions(db, md):

    print_step("[4] MAPPING: Role → Permissions")

    assert_ref(
        "role",
        "SUPER_ADMIN",
    )

    relation_t = table(
        md,
        "role_permissions",
    )

    created_count = 0

    for code, _ in PERMISSION_ROWS:

        assert_ref(
            "permission",
            code,
        )

        lookup = {
            "role_id": resolve(
                ref(
                    "role",
                    "SUPER_ADMIN",
                )
            ),
            "permission_id": resolve(
                ref(
                    "permission",
                    code,
                )
            ),
        }

        if not existing_row(
            db,
            relation_t,
            lookup,
        ):

            db.execute(
                relation_t.insert().values(
                    **lookup
                )
            )

            created_count += 1

    db.flush()

    print(
        f"  Role permissions created: {created_count}"
    )


# ============================================================================
# STEP 5 — SERVICE CATEGORY MASTER
# ============================================================================

def seed_service_categories(db, md):

    print_step("[5] MASTER: Service Categories")

    category_t = table(
        md,
        "service_categories",
    )

    for (
        name,
        slug,
        description,
        icon,
        display_order,
        active,
    ) in CATEGORY_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "service_categories",
            {
                "name": name,
                "slug": slug,
                "description": description,
                "icon": icon,
                "display_order": display_order,
                "is_active": active,
            },
            {
                "slug": slug,
            },
        )

        save_ref(
            "category",
            slug,
            row,
            category_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"category: {slug}"
        )


# ============================================================================
# STEP 6 — SERVICE MASTER
# ============================================================================

def seed_services(db, md):

    print_step("[6] MASTER: Services")

    service_t = table(
        md,
        "services",
    )

    for (
        category_slug,
        name,
        slug,
        short_description,
        long_description,
        starting_price,
        custom_quote,
        display_order,
    ) in SERVICE_ROWS:

        assert_ref(
            "category",
            category_slug,
        )

        row, created = insert_or_get(
            db,
            md,
            "services",
            {
                "category_id": ref(
                    "category",
                    category_slug,
                ),
                "name": name,
                "slug": slug,
                "short_description": short_description,
                "long_description": long_description,
                "starting_price": starting_price,
                "is_custom_quote_only": custom_quote,
                "is_active": True,
                "display_order": display_order,
                "meta_title": f"{name} | SS Platform",
                "meta_description": short_description,
            },
            {
                "slug": slug,
            },
        )

        save_ref(
            "service",
            slug,
            row,
            service_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"service: {slug}"
        )


# ============================================================================
# STEP 7 — TECHNOLOGY MASTER
# ============================================================================

def seed_technologies(db, md):

    print_step("[7] MASTER: Technologies")

    technology_t = table(
        md,
        "technologies",
    )

    for name, icon in TECHNOLOGY_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "technologies",
            {
                "name": name,
                "icon": icon,
            },
            {
                "name": name,
            },
        )

        save_ref(
            "technology",
            name,
            row,
            technology_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"technology: {name}"
        )


# ============================================================================
# STEP 8 — SERVICE/TECHNOLOGY MAPPING
# ============================================================================

def seed_service_technology_mappings(db, md):

    print_step(
        "[8] MAPPING: Service → Technologies"
    )

    relation_t = table(
        md,
        "service_technologies",
    )

    service_technology_map = {

        "website-development": [
            "React",
            "FastAPI",
            "MySQL",
            "Git",
        ],

        "e-commerce": [
            "React",
            "FastAPI",
            "MySQL",
            "AWS",
        ],

        "admin-panel": [
            "React",
            "FastAPI",
            "MySQL",
        ],

        "rest-api": [
            "FastAPI",
            "Python",
            "MySQL",
            "Docker",
        ],

        "mobile-application": [
            "Python",
            "FastAPI",
            "MySQL",
        ],

        "crm": [
            "React",
            "FastAPI",
            "MySQL",
        ],

        "hosting-deployment": [
            "Linux",
            "Nginx",
            "AWS",
            "Docker",
        ],

        "automation-integration": [
            "Python",
            "FastAPI",
            "Node.js",
        ],
    }

    created_count = 0

    for service_slug, technologies in (
        service_technology_map.items()
    ):

        assert_ref(
            "service",
            service_slug,
        )

        service_id = resolve(
            ref(
                "service",
                service_slug,
            )
        )

        for technology_name in technologies:

            assert_ref(
                "technology",
                technology_name,
            )

            technology_id = resolve(
                ref(
                    "technology",
                    technology_name,
                )
            )

            lookup = {
                "service_id": service_id,
                "technology_id": technology_id,
            }

            if not existing_row(
                db,
                relation_t,
                lookup,
            ):

                db.execute(
                    relation_t.insert().values(
                        **lookup
                    )
                )

                created_count += 1

    db.flush()

    print(
        f"  Service technology mappings created: "
        f"{created_count}"
    )


# ============================================================================
# STEP 9 — PAGE MASTER
# ============================================================================

def seed_pages(db, md):

    print_step("[9] MASTER: Pages")

    page_t = table(
        md,
        "pages",
    )

    for slug, title, published in PAGE_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "pages",
            {
                "slug": slug,
                "title": title,
                "is_published": published,
            },
            {
                "slug": slug,
            },
        )

        save_ref(
            "page",
            slug,
            row,
            page_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"page: {slug}"
        )


# ============================================================================
# STEP 10 — PAGE SECTIONS / WEBSITE CONTENT
# ============================================================================

def seed_page_sections(db, md):

    print_step(
        "[10] CONTENT: Page Sections"
    )

    sections = {

        "home": [
            (
                "hero",
                {
                    "heading": "Build. Automate. Grow.",
                    "cta": "/services",
                },
            ),
            (
                "services",
                {
                    "heading": "Technical Services",
                    "items": 8,
                },
            ),
            (
                "projects",
                {
                    "heading": "Selected Projects",
                    "items": 3,
                },
            ),
        ],

        "about": [
            (
                "intro",
                {
                    "heading": (
                        "Technology platform for modern businesses"
                    ),
                },
            ),
            (
                "values",
                {
                    "items": [
                        "Quality",
                        "Security",
                        "Maintainability",
                    ],
                },
            ),
        ],

        "services": [
            (
                "hero",
                {
                    "heading": (
                        "Website, Mobile, API and Business Solutions"
                    ),
                },
            ),
        ],

        "pricing": [
            (
                "plans",
                {
                    "currency": "INR",
                    "starting_from": 19999,
                },
            ),
        ],

        "contact": [
            (
                "contact",
                {
                    "email": ADMIN_EMAIL,
                    "phone": "+919999000001",
                },
            ),
        ],

        "blog": [
            (
                "hero",
                {
                    "heading": "Technology & Business Insights",
                },
            ),
        ],
    }

    section_t = table(
        md,
        "page_sections",
    )

    created_count = 0

    for page_slug, section_rows in sections.items():

        assert_ref(
            "page",
            page_slug,
        )

        for order, (
            section_type,
            content,
        ) in enumerate(
            section_rows,
            1,
        ):

            _, created = insert_or_get(
                db,
                md,
                "page_sections",
                {
                    "page_id": ref(
                        "page",
                        page_slug,
                    ),
                    "section_type": section_type,
                    "content_json": content,
                    "display_order": order,
                    "is_active": True,
                },
                {
                    "page_id": ref(
                        "page",
                        page_slug,
                    ),
                    "section_type": section_type,
                    "display_order": order,
                },
            )

            if created:
                created_count += 1

    print(
        f"  Page sections created: {created_count}"
    )


# ============================================================================
# STEP 11 — BANNERS
# ============================================================================

def seed_banners(db, md):

    print_step("[11] CONTENT: Banners")

    for (
        title,
        image,
        link,
        order,
        active,
    ) in BANNER_ROWS:

        _, created = insert_or_get(
            db,
            md,
            "banners",
            {
                "title": title,
                "image_url": image,
                "link_url": link,
                "display_order": order,
                "is_active": active,
                "starts_at": (
                    utcnow()
                    - timedelta(days=1)
                ),
                "ends_at": (
                    utcnow()
                    + timedelta(days=365)
                ),
            },
            {
                "title": title,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"banner: {title}"
        )


# ============================================================================
# STEP 12 — ANNOUNCEMENTS
# ============================================================================

def seed_announcements(db, md):

    print_step("[12] CONTENT: Announcements")

    for (
        message,
        link,
        active,
    ) in ANNOUNCEMENT_ROWS:

        _, created = insert_or_get(
            db,
            md,
            "announcements",
            {
                "message": message,
                "link_url": link,
                "is_active": active,
                "starts_at": (
                    utcnow()
                    - timedelta(days=1)
                ),
                "ends_at": (
                    utcnow()
                    + timedelta(days=365)
                ),
            },
            {
                "message": message,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"announcement"
        )


# ============================================================================
# STEP 13 — SEO / SETTINGS / SOCIAL / REDIRECTS
# ============================================================================

def seed_seo_settings_social(db, md):

    print_step(
        "[13] CONTENT: SEO / Settings / Social / Redirects"
    )

    seo_rows = [
        (
            "/",
            "SS Platform | Web, Mobile & API Development",
            (
                "Website, mobile app, admin panel, "
                "e-commerce and REST API development."
            ),
        ),
        (
            "/services",
            "Technical Services | SS Platform",
            (
                "React, FastAPI, Laravel, mobile, CRM, "
                "e-commerce and API services."
            ),
        ),
        (
            "/contact",
            "Contact | SS Platform",
            (
                "Contact SS Platform for website, "
                "software and business automation projects."
            ),
        ),
        (
            "/blog",
            "Technology Blog | SS Platform",
            (
                "Technology, software development "
                "and business automation articles."
            ),
        ),
    ]

    for path, title, description in seo_rows:

        _, created = insert_or_get(
            db,
            md,
            "seo_meta",
            {
                "path": path,
                "title": title,
                "description": description,
                "canonical_url": (
                    f"{DEMO_DOMAIN}{path}"
                ),
                "og_image_url": (
                    "/assets/img/og-image.jpg"
                ),
                "schema_json": {
                    "@context": "https://schema.org",
                    "@type": "WebSite",
                    "name": "SS Platform",
                    "url": DEMO_DOMAIN,
                },
            },
            {
                "path": path,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"SEO: {path}"
        )

    for (
        group,
        key,
        value,
        secret,
    ) in SETTING_ROWS:

        _, created = insert_or_get(
            db,
            md,
            "settings",
            {
                "group": group,
                "key": key,
                "value": value,
                "is_secret": secret,
            },
            {
                "group": group,
                "key": key,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"setting: {group}.{key}"
        )

    for platform, url, active in SOCIAL_ROWS:

        _, created = insert_or_get(
            db,
            md,
            "social_links",
            {
                "platform": platform,
                "url": url,
                "is_active": active,
            },
            {
                "platform": platform,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"social: {platform}"
        )

    for (
        from_path,
        to_path,
        status_code,
        active,
    ) in REDIRECT_ROWS:

        _, created = insert_or_get(
            db,
            md,
            "redirects",
            {
                "from_path": from_path,
                "to_path": to_path,
                "status_code": status_code,
                "is_active": active,
            },
            {
                "from_path": from_path,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"redirect: {from_path}"
        )


# ============================================================================
# STEP 14 — BLOG CATEGORY MASTER
# ============================================================================

def seed_blog_categories(db, md):

    print_step(
        "[14] MASTER: Blog Categories"
    )

    blog_category_t = table(
        md,
        "blog_categories",
    )

    for name, slug in BLOG_CATEGORY_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "blog_categories",
            {
                "name": name,
                "slug": slug,
            },
            {
                "slug": slug,
            },
        )

        save_ref(
            "blog_category",
            slug,
            row,
            blog_category_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"blog category: {slug}"
        )


# ============================================================================
# STEP 15 — BLOG TAG MASTER
# ============================================================================

def seed_blog_tags(db, md):

    print_step(
        "[15] MASTER: Blog Tags"
    )

    blog_tag_t = table(
        md,
        "blog_tags",
    )

    for name in BLOG_TAG_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "blog_tags",
            {
                "name": name,
            },
            {
                "name": name,
            },
        )

        save_ref(
            "blog_tag",
            name,
            row,
            blog_tag_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"blog tag: {name}"
        )


# ============================================================================
# STEP 16 — PROJECTS / TEAM / TESTIMONIALS
# ============================================================================

def seed_projects_team_testimonials(db, md):

    print_step(
        "[16] CONTENT: Projects / Team / Testimonials"
    )

    for (
        title,
        slug,
        summary,
        tech,
        status,
        featured,
    ) in PROJECT_ROWS:

        _, created = insert_or_get(
            db,
            md,
            "projects",
            {
                "title": title,
                "slug": slug,
                "summary": summary,
                "description": summary,
                "tech_stack": tech,
                "cover_image_url": (
                    "/assets/img/project-placeholder.jpg"
                ),
                "live_url": DEMO_DOMAIN,
                "status": status,
                "is_featured": featured,
                "is_active": True,
                "display_order": 1,
            },
            {
                "slug": slug,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"project: {slug}"
        )

    team_rows = [
        (
            "Saurabh Shukla",
            "CTO — SS Collections Group",
            (
                "Leads technology strategy and platform development "
                "for SS Collections Group and client projects."
            ),
            "/assets/img/team/saurabh.jpg",
        ),
        (
            "SS Platform Team",
            "Engineering",
            (
                "Demo engineering team responsible for web, API, "
                "mobile and business platform delivery."
            ),
            None,
        ),
    ]

    for index, (
        name,
        role,
        bio,
        photo,
    ) in enumerate(
        team_rows,
        1,
    ):

        _, created = insert_or_get(
            db,
            md,
            "team_members",
            {
                "full_name": name,
                "role_title": role,
                "bio": bio,
                "photo_url": photo,
                "display_order": index,
                "is_active": True,
            },
            {
                "full_name": name,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"team member: {name}"
        )

    for index, (
        name,
        company,
        quote,
        rating,
    ) in enumerate(
        TESTIMONIAL_ROWS,
        1,
    ):

        _, created = insert_or_get(
            db,
            md,
            "testimonials",
            {
                "client_name": name,
                "client_company": company,
                "photo_url": None,
                "quote": quote,
                "rating": rating,
                "is_active": True,
                "display_order": index,
            },
            {
                "client_name": name,
                "client_company": company,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"testimonial: {name}"
        )


# ============================================================================
# STEP 17 — BLOG MASTER RECORDS
# ============================================================================

def seed_blogs(db, md):

    print_step(
        "[17] MASTER/CONTENT: Blogs"
    )

    assert_ref(
        "admin",
        ADMIN_EMAIL,
    )

    blogs = [
        (
            "Getting Started with React and FastAPI",
            "react-fastapi-starter",
            (
                "How a React frontend and FastAPI backend "
                "can be combined for a modern application."
            ),
            (
                "React provides the user interface while FastAPI "
                "provides typed, documented APIs."
            ),
            "web-development",
        ),
        (
            "Building a Reliable E-Commerce Backend",
            "reliable-ecommerce-backend",
            (
                "Important backend components "
                "for an online store."
            ),
            (
                "Catalogue, inventory, orders, payments, customers "
                "and audit trails should be designed together."
            ),
            "e-commerce",
        ),
        (
            "Why Business Automation Matters",
            "business-automation-basics",
            (
                "Practical areas where small businesses "
                "can reduce manual work."
            ),
            (
                "Lead management, notifications, reporting "
                "and integrations are common automation opportunities."
            ),
            "business-automation",
        ),
    ]

    blog_t = table(
        md,
        "blogs",
    )

    for (
        title,
        slug,
        excerpt,
        content,
        category_slug,
    ) in blogs:

        assert_ref(
            "blog_category",
            category_slug,
        )

        row, created = insert_or_get(
            db,
            md,
            "blogs",
            {
                "category_id": ref(
                    "blog_category",
                    category_slug,
                ),
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "title": title,
                "slug": slug,
                "excerpt": excerpt,
                "content": content,
                "cover_image_url": (
                    "/assets/img/blog-placeholder.jpg"
                ),
                "is_published": True,
                "published_at": (
                    utcnow()
                    - timedelta(days=2)
                ),
                "meta_title": title,
                "meta_description": excerpt,
            },
            {
                "slug": slug,
            },
        )

        save_ref(
            "blog",
            slug,
            row,
            blog_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"blog: {slug}"
        )


# ============================================================================
# STEP 18 — BLOG TAG MAPPING
# ============================================================================

def seed_blog_tag_mappings(db, md):

    print_step(
        "[18] MAPPING: Blog → Tags"
    )

    blog_tag_map_t = table(
        md,
        "blog_tag_map",
    )

    blog_tags = {

        "react-fastapi-starter": [
            "React",
            "FastAPI",
            "Python",
        ],

        "reliable-ecommerce-backend": [
            "E-Commerce",
            "MySQL",
            "REST API",
        ],

        "business-automation-basics": [
            "Automation",
            "CRM",
        ],
    }

    created_count = 0

    for blog_slug, tags in blog_tags.items():

        assert_ref(
            "blog",
            blog_slug,
        )

        for tag_name in tags:

            assert_ref(
                "blog_tag",
                tag_name,
            )

            lookup = {
                "blog_id": resolve(
                    ref(
                        "blog",
                        blog_slug,
                    )
                ),
                "tag_id": resolve(
                    ref(
                        "blog_tag",
                        tag_name,
                    )
                ),
            }

            if not existing_row(
                db,
                blog_tag_map_t,
                lookup,
            ):

                db.execute(
                    blog_tag_map_t.insert().values(
                        **lookup
                    )
                )

                created_count += 1

    db.flush()

    print(
        f"  Blog tag mappings created: {created_count}"
    )


# ============================================================================
# STEP 19 — SERVICE PACKAGES MASTER
# ============================================================================

def seed_service_packages(db, md):

    print_step(
        "[19] MASTER: Service Packages"
    )

    package_specs = [
        (
            "website-development",
            "Starter Website",
            Decimal("19999"),
            False,
            "one_time",
            (
                "Responsive frontend, backend API "
                "and basic admin panel."
            ),
            1,
        ),
        (
            "website-development",
            "Business Website",
            Decimal("29999"),
            False,
            "one_time",
            (
                "Business website with CMS, inquiry "
                "forms and SEO setup."
            ),
            2,
        ),
        (
            "e-commerce",
            "E-Commerce Starter",
            Decimal("49999"),
            False,
            "one_time",
            (
                "Storefront, catalogue, cart, checkout "
                "and order management."
            ),
            1,
        ),
        (
            "e-commerce",
            "E-Commerce Pro",
            Decimal("79999"),
            False,
            "one_time",
            (
                "Advanced store with payment integration, "
                "inventory and reporting."
            ),
            2,
        ),
        (
            "admin-panel",
            "Admin Panel Standard",
            Decimal("24999"),
            False,
            "one_time",
            (
                "Role-based dashboard, CRUD modules and reports."
            ),
            1,
        ),
        (
            "rest-api",
            "API Development",
            Decimal("29999"),
            False,
            "one_time",
            (
                "Documented REST API with authentication "
                "and database integration."
            ),
            1,
        ),
        (
            "crm",
            "CRM Starter",
            Decimal("34999"),
            False,
            "one_time",
            (
                "Customers, inquiries, leads and follow-ups."
            ),
            1,
        ),
        (
            "hosting-deployment",
            "Managed Maintenance",
            Decimal("4999"),
            False,
            "monthly",
            (
                "Deployment, SSL, uptime checks and maintenance."
            ),
            1,
        ),
    ]

    for (
        service_slug,
        name,
        price,
        custom_quote,
        interval,
        description,
        display_order,
    ) in package_specs:

        assert_ref(
            "service",
            service_slug,
        )

        _, created = insert_or_get(
            db,
            md,
            "service_packages",
            {
                "service_id": ref(
                    "service",
                    service_slug,
                ),
                "name": name,
                "price": price,
                "is_custom_quote": custom_quote,
                "billing_interval": interval,
                "description": description,
                "is_active": True,
                "display_order": display_order,
            },
            {
                "service_id": ref(
                    "service",
                    service_slug,
                ),
                "name": name,
            },
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"package: {name}"
        )


# ============================================================================
# STEP 20 — SERVICE FEATURES MASTER
# ============================================================================

def seed_service_features(db, md):

    print_step(
        "[20] MASTER: Service Features"
    )

    feature_map = {

        "website-development": [
            "Responsive UI",
            "REST API",
            "Admin Panel",
            "SEO Ready",
        ],

        "e-commerce": [
            "Product Catalogue",
            "Cart & Checkout",
            "Order Management",
            "Payment Integration",
        ],

        "admin-panel": [
            "Authentication",
            "Role Permissions",
            "Dashboard",
            "Reports",
        ],

        "rest-api": [
            "JWT Authentication",
            "Swagger Docs",
            "Validation",
            "MySQL Integration",
        ],

        "mobile-application": [
            "API Integration",
            "Authentication",
            "Push Notifications",
        ],

        "crm": [
            "Customers",
            "Lead Pipeline",
            "Follow-ups",
            "Notes",
        ],

        "hosting-deployment": [
            "SSL",
            "Nginx",
            "Deployment",
            "Monitoring",
        ],

        "automation-integration": [
            "API Integration",
            "Scheduled Jobs",
            "Notifications",
        ],
    }

    for service_slug, features in feature_map.items():

        assert_ref(
            "service",
            service_slug,
        )

        for order, title in enumerate(
            features,
            1,
        ):

            insert_or_get(
                db,
                md,
                "service_features",
                {
                    "service_id": ref(
                        "service",
                        service_slug,
                    ),
                    "title": title,
                    "display_order": order,
                },
                {
                    "service_id": ref(
                        "service",
                        service_slug,
                    ),
                    "title": title,
                },
            )


# ============================================================================
# STEP 21 — FAQ MASTER
# ============================================================================

def seed_faqs(db, md):

    print_step(
        "[21] MASTER: FAQs"
    )

    faq_rows = [
        (
            "website-development",
            "Is the website responsive?",
            (
                "Yes. The demo package is intended for mobile, "
                "tablet and desktop layouts."
            ),
        ),
        (
            "e-commerce",
            "Can the store manage orders?",
            (
                "Yes. Orders, payments and invoices are "
                "represented in the platform database."
            ),
        ),
        (
            "rest-api",
            "Is Swagger documentation available?",
            (
                "FastAPI exposes interactive OpenAPI documentation."
            ),
        ),
        (
            "crm",
            "Can leads have follow-ups?",
            (
                "Yes. Leads support follow-ups, notes "
                "and status history."
            ),
        ),
        (
            "hosting-deployment",
            "Can SSL be configured?",
            (
                "Yes. SSL and deployment are included "
                "in the demo service description."
            ),
        ),
    ]

    for (
        service_slug,
        question,
        answer,
    ) in faq_rows:

        assert_ref(
            "service",
            service_slug,
        )

        insert_or_get(
            db,
            md,
            "faqs",
            {
                "question": question,
                "answer": answer,
                "service_id": ref(
                    "service",
                    service_slug,
                ),
                "display_order": 1,
                "is_active": True,
            },
            {
                "question": question,
            },
        )


# ============================================================================
# STEP 22 — SERVICE TOKEN MASTER
# ============================================================================

def seed_service_tokens(db, md):

    print_step(
        "[22] MASTER: Service Tokens"
    )

    token_rows = [
        (
            "Website Token",
            "One unit of website development work",
            Decimal("1000"),
        ),
        (
            "API Token",
            "One unit of API development work",
            Decimal("1500"),
        ),
        (
            "Support Token",
            "One unit of support/maintenance work",
            Decimal("500"),
        ),
    ]

    for name, description, value in token_rows:

        insert_or_get(
            db,
            md,
            "service_tokens",
            {
                "name": name,
                "description": description,
                "token_value_inr": value,
            },
            {
                "name": name,
            },
        )


# ============================================================================
# STEP 23 — OFFERS MASTER
# ============================================================================

def seed_offers(db, md):

    print_step(
        "[23] MASTER: Offers"
    )

    offer_rows = [
        (
            "Website Launch Offer",
            "Complete frontend + backend website package.",
            "website-development",
            "Starting from ₹19,999",
        ),
        (
            "E-Commerce Setup Offer",
            "Launch an online store with catalogue and checkout.",
            "e-commerce",
            "Save on initial setup",
        ),
        (
            "CRM Setup Offer",
            "Customer and lead management for service businesses.",
            "crm",
            "Demo package available",
        ),
    ]

    for (
        title,
        description,
        service_slug,
        discount_label,
    ) in offer_rows:

        assert_ref(
            "service",
            service_slug,
        )

        insert_or_get(
            db,
            md,
            "offers",
            {
                "title": title,
                "description": description,
                "service_id": ref(
                    "service",
                    service_slug,
                ),
                "discount_label": discount_label,
                "is_active": True,
                "starts_at": (
                    utcnow()
                    - timedelta(days=1)
                ),
                "ends_at": (
                    utcnow()
                    + timedelta(days=90)
                ),
            },
            {
                "title": title,
            },
        )


# ============================================================================
# STEP 24 — COUPON MASTER
# ============================================================================

def seed_coupons(db, md):

    print_step(
        "[24] MASTER: Coupons"
    )

    coupon_specs = [
        (
            "WELCOME10",
            "10 percent demo welcome discount",
            "PERCENT",
            Decimal("10.00"),
        ),
        (
            "WEB5000",
            "₹5,000 demo website discount",
            "FIXED",
            Decimal("5000.00"),
        ),
        (
            "CRM10",
            "10 percent demo CRM discount",
            "PERCENT",
            Decimal("10.00"),
        ),
    ]

    for (
        code,
        description,
        discount_type,
        discount_value,
    ) in coupon_specs:

        insert_or_get(
            db,
            md,
            "coupons",
            {
                "code": code,
                "description": description,
                "discount_type": discount_type,
                "discount_value": discount_value,
                "max_uses": 100,
                "valid_from": (
                    utcnow()
                    - timedelta(days=1)
                ),
                "valid_until": (
                    utcnow()
                    + timedelta(days=90)
                ),
                "is_active": True,
            },
            {
                "code": code,
            },
        )


# ============================================================================
# STEP 25 — USERS MASTER
# ============================================================================

def seed_users(db, md):

    print_step(
        "[25] MASTER: Users"
    )

    user_t = table(
        md,
        "users",
    )

    for name, email, phone in USER_ROWS:

        row, created = insert_or_get(
            db,
            md,
            "users",
            {
                "full_name": name,
                "email": email,
                "phone": phone,
                "hashed_password": hash_password(
                    "Demo123!"
                ),
                "is_active": True,
            },
            {
                "email": email,
            },
        )

        save_ref(
            "user",
            email,
            row,
            user_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"user: {email}"
        )


# ============================================================================
# STEP 26 — CUSTOMER MASTER
# ============================================================================

def seed_customers(db, md):

    print_step(
        "[26] MASTER: Customers"
    )

    customer_t = table(
        md,
        "customers",
    )

    for (
        name,
        email,
        phone,
        company,
    ) in CUSTOMER_ROWS:

        assert_ref(
            "user",
            email,
        )

        row, created = insert_or_get(
            db,
            md,
            "customers",
            {
                "user_id": ref(
                    "user",
                    email,
                ),
                "full_name": name,
                "email": email,
                "phone": phone,
                "company_name": company,
                "notes": (
                    "Demo customer created by SS Platform seeder."
                ),
            },
            {
                "email": email,
            },
        )

        save_ref(
            "customer",
            email,
            row,
            customer_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"customer: {email}"
        )


# ============================================================================
# STEP 27 — SUBSCRIPTION PLAN MASTER
# ============================================================================

def seed_subscription_plans(db, md):

    print_step(
        "[27] MASTER: Subscription Plans"
    )

    plan_t = table(
        md,
        "subscription_plans",
    )

    plans = [
        (
            "website-development",
            "Website Care Monthly",
            Decimal("2499"),
            "MONTHLY",
            (
                "Monthly website maintenance, "
                "updates and support."
            ),
        ),
        (
            "hosting-deployment",
            "Managed Hosting Yearly",
            Decimal("49999"),
            "YEARLY",
            (
                "Managed hosting, SSL, deployment "
                "and maintenance."
            ),
        ),
        (
            "crm",
            "CRM Monthly",
            Decimal("3999"),
            "MONTHLY",
            (
                "CRM support and monthly maintenance."
            ),
        ),
    ]

    for (
        service_slug,
        name,
        price,
        interval,
        features,
    ) in plans:

        assert_ref(
            "service",
            service_slug,
        )

        row, created = insert_or_get(
            db,
            md,
            "subscription_plans",
            {
                "service_id": ref(
                    "service",
                    service_slug,
                ),
                "name": name,
                "price": price,
                "billing_interval": interval,
                "features": features,
                "is_active": True,
            },
            {
                "name": name,
            },
        )

        save_ref(
            "plan",
            name,
            row,
            plan_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"plan: {name}"
        )


# ============================================================================
# STEP 28 — INQUIRIES
# ============================================================================

def seed_inquiries(db, md):

    print_step(
        "[28] BUSINESS: Inquiries"
    )

    service_by_name = {
        row[1]: row[2]
        for row in SERVICE_ROWS
    }

    inquiry_specs = [
        (
            "customer1@example.com",
            "Website Development",
            "₹20,000 - ₹30,000",
            "2-4 weeks",
            "email",
            (
                "Need a responsive business website "
                "with admin panel."
            ),
        ),
        (
            "customer2@example.com",
            "E-Commerce",
            "₹50,000 - ₹80,000",
            "4-8 weeks",
            "whatsapp",
            (
                "Need an online store with catalogue "
                "and payment gateway."
            ),
        ),
        (
            "owner@example.com",
            "CRM",
            "₹25,000 - ₹40,000",
            "3-6 weeks",
            "phone",
            (
                "Need CRM for inquiries, leads and follow-ups."
            ),
        ),
        (
            "founder@example.com",
            "REST API",
            "₹20,000 - ₹40,000",
            "2-5 weeks",
            "email",
            (
                "Need documented REST API with JWT authentication."
            ),
        ),
    ]

    inquiry_t = table(
        md,
        "inquiries",
    )

    for index, (
        email,
        service_name,
        budget,
        timeline,
        contact,
        message,
    ) in enumerate(
        inquiry_specs,
        1,
    ):

        assert_ref(
            "customer",
            email,
        )

        service_slug = service_by_name[
            service_name
        ]

        assert_ref(
            "service",
            service_slug,
        )

        row, created = insert_or_get(
            db,
            md,
            "inquiries",
            {
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "full_name": f"Demo Inquiry {index}",
                "email": email,
                "phone": (
                    f"+9199990002{index:02d}"
                ),
                "service_id": ref(
                    "service",
                    service_slug,
                ),
                "budget_range": budget,
                "timeline": timeline,
                "preferred_contact_method": contact,
                "message": message,
                "source": "website",
            },
            {
                "email": email,
                "message": message,
            },
        )

        save_ref(
            "inquiry",
            index,
            row,
            inquiry_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"inquiry: {index}"
        )


# ============================================================================
# STEP 29 — LEADS
# ============================================================================

def seed_leads(db, md):

    print_step(
        "[29] BUSINESS: Leads"
    )

    lead_t = table(
        md,
        "leads",
    )

    lead_specs = [
        (
            1,
            "customer1@example.com",
            "NEW",
            Decimal("25000"),
        ),
        (
            2,
            "customer2@example.com",
            "QUALIFIED",
            Decimal("65000"),
        ),
        (
            3,
            "owner@example.com",
            "PROPOSAL_SENT",
            Decimal("35000"),
        ),
        (
            4,
            "founder@example.com",
            "NEGOTIATION",
            Decimal("30000"),
        ),
    ]

    for (
        inquiry_no,
        email,
        status,
        estimated_value,
    ) in lead_specs:

        assert_ref(
            "inquiry",
            inquiry_no,
        )

        assert_ref(
            "customer",
            email,
        )

        assert_ref(
            "admin",
            ADMIN_EMAIL,
        )

        row, created = insert_or_get(
            db,
            md,
            "leads",
            {
                "inquiry_id": ref(
                    "inquiry",
                    inquiry_no,
                ),
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "assigned_admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "status": status,
                "source": "website",
                "estimated_value": estimated_value,
            },
            {
                "inquiry_id": ref(
                    "inquiry",
                    inquiry_no,
                ),
            },
        )

        save_ref(
            "lead",
            inquiry_no,
            row,
            lead_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"lead: {inquiry_no}"
        )


# ============================================================================
# STEP 30 — CUSTOMER WALLETS
# ============================================================================

def seed_customer_wallets(db, md):

    print_step(
        "[30] MASTER/BUSINESS: Customer Wallets"
    )

    wallet_t = table(
        md,
        "customer_wallets",
    )

    for (
        _name,
        email,
        _phone,
        _company,
    ) in CUSTOMER_ROWS:

        assert_ref(
            "customer",
            email,
        )

        row, created = insert_or_get(
            db,
            md,
            "customer_wallets",
            {
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "token_balance": 100,
            },
            {
                "customer_id": ref(
                    "customer",
                    email,
                ),
            },
        )

        save_ref(
            "wallet",
            email,
            row,
            wallet_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"wallet: {email}"
        )


# ============================================================================
# STEP 31 — VISITORS
# ============================================================================

def seed_visitors(db, md):

    print_step(
        "[31] ANALYTICS: Visitors"
    )

    visitor_rows = [
        (
            "192.168.1.101",
            "Chrome",
            "153",
            "Windows",
            "Desktop",
            1920,
            1080,
        ),
        (
            "192.168.1.102",
            "Chrome",
            "153",
            "Android",
            "Mobile",
            412,
            915,
        ),
        (
            "192.168.1.103",
            "Edge",
            "153",
            "Windows",
            "Desktop",
            1920,
            1080,
        ),
        (
            "192.168.1.104",
            "Safari",
            "18",
            "iOS",
            "Mobile",
            390,
            844,
        ),
        (
            "192.168.1.105",
            "Chrome",
            "153",
            "macOS",
            "Desktop",
            1440,
            900,
        ),
    ]

    visitor_t = table(
        md,
        "visitors",
    )

    for index, (
        ip,
        browser,
        browser_version,
        os_name,
        device,
        width,
        height,
    ) in enumerate(
        visitor_rows,
        1,
    ):

        visitor_uuid = (
            f"00000000-0000-4000-8000-{index:012d}"
        )

        row, created = insert_or_get(
            db,
            md,
            "visitors",
            {
                "visitor_uuid": visitor_uuid,
                "ip_address": ip,
                "browser": browser,
                "browser_version": browser_version,
                "os": os_name,
                "device": device,
                "screen_width": width,
                "screen_height": height,
            },
            {
                "visitor_uuid": visitor_uuid,
            },
        )

        save_ref(
            "visitor",
            index,
            row,
            visitor_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"visitor: {index}"
        )


# ============================================================================
# STEP 32 — VISITOR SESSIONS
# ============================================================================

def seed_visitor_sessions(db, md):

    print_step(
        "[32] ANALYTICS: Visitor Sessions"
    )

    session_rows = [
        (
            1,
            "/",
            "/services",
            "https://google.com",
            "google",
            "organic",
            None,
            35,
        ),
        (
            2,
            "/services",
            "/contact",
            DEMO_DOMAIN,
            "instagram",
            "social",
            "launch",
            82,
        ),
        (
            3,
            "/",
            "/pricing",
            DEMO_DOMAIN,
            "direct",
            "none",
            None,
            140,
        ),
        (
            4,
            "/blog",
            "/services",
            "https://instagram.com",
            "instagram",
            "social",
            "services",
            55,
        ),
        (
            5,
            "/contact",
            "/contact",
            None,
            "direct",
            "none",
            None,
            210,
        ),
    ]

    session_t = table(
        md,
        "visitor_sessions",
    )

    for index, (
        visitor_no,
        landing,
        exit_page,
        referrer,
        source,
        medium,
        campaign,
        duration,
    ) in enumerate(
        session_rows,
        1,
    ):

        assert_ref(
            "visitor",
            visitor_no,
        )

        session_uuid = (
            f"00000000-1111-4000-8000-{index:012d}"
        )

        started = (
            utcnow()
            - timedelta(
                minutes=20 + index * 7
            )
        )

        ended = (
            started
            + timedelta(
                seconds=duration
            )
        )

        row, created = insert_or_get(
            db,
            md,
            "visitor_sessions",
            {
                "visitor_id": ref(
                    "visitor",
                    visitor_no,
                ),
                "session_uuid": session_uuid,
                "landing_page": landing,
                "exit_page": exit_page,
                "referrer": referrer,
                "utm_source": source,
                "utm_medium": medium,
                "utm_campaign": campaign,
                "utm_term": None,
                "utm_content": None,
                "started_at": started,
                "ended_at": ended,
                "duration_seconds": duration,
            },
            {
                "session_uuid": session_uuid,
            },
        )

        save_ref(
            "session",
            index,
            row,
            session_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"session: {index}"
        )


# ============================================================================
# STEP 33 — ANALYTICS EVENTS
# ============================================================================

def seed_analytics_events(db, md):

    print_step(
        "[33] ANALYTICS: Events"
    )

    event_specs = [
        (
            1,
            "page_view",
            "/",
            {"title": "Home"},
        ),
        (
            1,
            "click",
            "/services",
            {"element": "services-cta"},
        ),
        (
            2,
            "page_view",
            "/services",
            {"title": "Services"},
        ),
        (
            2,
            "inquiry_started",
            "/contact",
            {"service": "Website Development"},
        ),
        (
            3,
            "page_view",
            "/pricing",
            {"title": "Pricing"},
        ),
        (
            4,
            "page_view",
            "/blog",
            {"title": "Blog"},
        ),
        (
            5,
            "form_submit",
            "/contact",
            {"status": "demo"},
        ),
    ]

    for (
        session_no,
        event_type,
        page_url,
        metadata_json,
    ) in event_specs:

        assert_ref(
            "session",
            session_no,
        )

        insert_or_get(
            db,
            md,
            "analytics_events",
            {
                "session_id": ref(
                    "session",
                    session_no,
                ),
                "event_type": event_type,
                "page_url": page_url,
                "metadata_json": metadata_json,
            },
            {
                "session_id": ref(
                    "session",
                    session_no,
                ),
                "event_type": event_type,
                "page_url": page_url,
            },
        )


# ============================================================================
# STEP 34 — PAGE VIEWS
# ============================================================================

def seed_page_views(db, md):

    print_step(
        "[34] ANALYTICS: Page Views"
    )

    page_view_specs = [
        (1, "/", 25),
        (1, "/services", 10),
        (2, "/services", 60),
        (2, "/contact", 22),
        (3, "/", 45),
        (3, "/pricing", 95),
        (4, "/blog", 40),
        (5, "/contact", 180),
    ]

    for index, (
        session_no,
        page_url,
        duration,
    ) in enumerate(
        page_view_specs,
        1,
    ):

        assert_ref(
            "session",
            session_no,
        )

        entry = (
            utcnow()
            - timedelta(
                minutes=index * 9
            )
        )

        insert_or_get(
            db,
            md,
            "page_views",
            {
                "session_id": ref(
                    "session",
                    session_no,
                ),
                "page_url": page_url,
                "entry_time": entry,
                "exit_time": (
                    entry
                    + timedelta(
                        seconds=duration
                    )
                ),
                "duration_seconds": duration,
            },
            {
                "session_id": ref(
                    "session",
                    session_no,
                ),
                "page_url": page_url,
                "entry_time": entry,
            },
        )


# ============================================================================
# STEP 35 — ORDERS
# ============================================================================

def seed_orders(db, md):

    print_step(
        "[35] SALES: Orders"
    )

    package_t = table(
        md,
        "service_packages",
    )

    def get_package_id(name: str):

        row = existing_row(
            db,
            package_t,
            {
                "name": name,
            },
        )

        if not row:
            raise RuntimeError(
                f"Service package not found: {name}"
            )

        return row[
            pk_name(package_t)
        ]

    order_specs = [
        (
            "customer1@example.com",
            "Starter Website",
            None,
            "SS-DEMO-0001",
            Decimal("19999"),
            Decimal("0"),
            Decimal("19999"),
            "PENDING",
        ),
        (
            "customer2@example.com",
            "E-Commerce Starter",
            None,
            "SS-DEMO-0002",
            Decimal("49999"),
            Decimal("5000"),
            Decimal("44999"),
            "PAID",
        ),
        (
            "owner@example.com",
            "CRM Starter",
            None,
            "SS-DEMO-0003",
            Decimal("34999"),
            Decimal("0"),
            Decimal("34999"),
            "PAID",
        ),
        (
            "founder@example.com",
            None,
            "Website Care Monthly",
            "SS-DEMO-0004",
            Decimal("2499"),
            Decimal("0"),
            Decimal("2499"),
            "PENDING",
        ),
    ]

    order_t = table(
        md,
        "orders",
    )

    for (
        email,
        package_name,
        plan_name,
        order_number,
        subtotal,
        discount,
        total,
        status,
    ) in order_specs:

        assert_ref(
            "customer",
            email,
        )

        if package_name:
            package_id = get_package_id(
                package_name
            )
        else:
            package_id = None

        if plan_name:
            assert_ref(
                "plan",
                plan_name,
            )

        row, created = insert_or_get(
            db,
            md,
            "orders",
            {
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "service_package_id": package_id,
                "subscription_plan_id": (
                    ref(
                        "plan",
                        plan_name,
                    )
                    if plan_name
                    else None
                ),
                "order_number": order_number,
                "subtotal_amount": subtotal,
                "discount_amount": discount,
                "total_amount": total,
                "coupon_id": None,
                "status": status,
            },
            {
                "order_number": order_number,
            },
        )

        save_ref(
            "order",
            order_number,
            row,
            order_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"order: {order_number}"
        )


# ============================================================================
# STEP 36 — PAYMENTS
# ============================================================================

def seed_payments(db, md):

    print_step(
        "[36] SALES: Payments"
    )

    payment_specs = [
        (
            "SS-DEMO-0002",
            "DEMO",
            "DEMO-ORDER-2",
            "DEMO-PAY-2",
            Decimal("44999"),
            "INR",
            "SUCCESS",
        ),
        (
            "SS-DEMO-0003",
            "DEMO",
            "DEMO-ORDER-3",
            "DEMO-PAY-3",
            Decimal("34999"),
            "INR",
            "SUCCESS",
        ),
        (
            "SS-DEMO-0004",
            "DEMO",
            "DEMO-ORDER-4",
            None,
            Decimal("2499"),
            "INR",
            "PENDING",
        ),
    ]

    payment_t = table(
        md,
        "payments",
    )

    for (
        order_number,
        gateway,
        gateway_order_id,
        gateway_payment_id,
        amount,
        currency,
        status,
    ) in payment_specs:

        assert_ref(
            "order",
            order_number,
        )

        lookup = {
            "order_id": ref(
                "order",
                order_number,
            ),
            "gateway_order_id": gateway_order_id,
        }

        row, created = insert_or_get(
            db,
            md,
            "payments",
            {
                "order_id": ref(
                    "order",
                    order_number,
                ),
                "gateway": gateway,
                "gateway_order_id": gateway_order_id,
                "gateway_payment_id": gateway_payment_id,
                "amount": amount,
                "currency": currency,
                "status": status,
            },
            lookup,
        )

        save_ref(
            "payment",
            order_number,
            row,
            payment_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"payment: {order_number}"
        )


# ============================================================================
# STEP 37 — INVOICES
# ============================================================================

def seed_invoices(db, md):

    print_step(
        "[37] SALES: Invoices"
    )

    invoice_rows = [
        (
            "SS-DEMO-0002",
            "INV-DEMO-0002",
        ),
        (
            "SS-DEMO-0003",
            "INV-DEMO-0003",
        ),
    ]

    for order_number, invoice_number in invoice_rows:

        assert_ref(
            "order",
            order_number,
        )

        insert_or_get(
            db,
            md,
            "invoices",
            {
                "order_id": ref(
                    "order",
                    order_number,
                ),
                "invoice_number": invoice_number,
                "issued_at": (
                    utcnow()
                    - timedelta(days=1)
                ),
                "pdf_url": (
                    f"{DEMO_DOMAIN}/invoices/"
                    f"{invoice_number}.pdf"
                ),
            },
            {
                "invoice_number": invoice_number,
            },
        )


# ============================================================================
# STEP 38 — SUBSCRIPTIONS
# ============================================================================

def seed_subscriptions(db, md):

    print_step(
        "[38] SALES: Subscriptions"
    )

    subscription_specs = [
        (
            "customer1@example.com",
            "Website Care Monthly",
            "ACTIVE",
            30,
        ),
        (
            "founder@example.com",
            "Website Care Monthly",
            "ACTIVE",
            20,
        ),
        (
            "owner@example.com",
            "CRM Monthly",
            "PAST_DUE",
            -5,
        ),
    ]

    subscription_t = table(
        md,
        "subscriptions",
    )

    for index, (
        email,
        plan_name,
        status,
        days,
    ) in enumerate(
        subscription_specs,
        1,
    ):

        assert_ref(
            "customer",
            email,
        )

        assert_ref(
            "plan",
            plan_name,
        )

        start = (
            utcnow()
            - timedelta(days=30)
        )

        end = (
            utcnow()
            + timedelta(days=days)
        )

        row, created = insert_or_get(
            db,
            md,
            "subscriptions",
            {
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "plan_id": ref(
                    "plan",
                    plan_name,
                ),
                "status": status,
                "start_date": start,
                "end_date": end,
                "next_renewal_date": (
                    utcnow()
                    + timedelta(days=30)
                ),
                "auto_renew": True,
            },
            {
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "plan_id": ref(
                    "plan",
                    plan_name,
                ),
            },
        )

        save_ref(
            "subscription",
            index,
            row,
            subscription_t,
        )

        print(
            f"  {'CREATED' if created else 'EXISTS '} "
            f"subscription: {index}"
        )


# ============================================================================
# STEP 39 — SUBSCRIPTION ITEMS
# ============================================================================

def seed_subscription_items(db, md):

    print_step(
        "[39] SALES: Subscription Items"
    )

    subscription_item_rows = [
        (
            1,
            "Monthly website maintenance",
            1,
            Decimal("2499"),
        ),
        (
            1,
            "Priority support",
            1,
            Decimal("999"),
        ),
        (
            3,
            "CRM support",
            1,
            Decimal("3999"),
        ),
    ]

    for (
        subscription_no,
        label,
        quantity,
        unit_price,
    ) in subscription_item_rows:

        assert_ref(
            "subscription",
            subscription_no,
        )

        insert_or_get(
            db,
            md,
            "subscription_items",
            {
                "subscription_id": ref(
                    "subscription",
                    subscription_no,
                ),
                "label": label,
                "quantity": quantity,
                "unit_price": unit_price,
            },
            {
                "subscription_id": ref(
                    "subscription",
                    subscription_no,
                ),
                "label": label,
            },
        )


# ============================================================================
# STEP 40 — LEAD NOTES
# ============================================================================

def seed_lead_notes(db, md):

    print_step(
        "[40] CRM: Lead Notes"
    )

    lead_notes = [
        (
            1,
            "Initial inquiry received from website contact form.",
        ),
        (
            2,
            "Customer confirmed budget and requested payment integration.",
        ),
        (
            3,
            "Proposal shared; waiting for final scope approval.",
        ),
        (
            4,
            "Discussed API modules and delivery milestones.",
        ),
    ]

    for lead_no, note in lead_notes:

        assert_ref(
            "lead",
            lead_no,
        )

        insert_or_get(
            db,
            md,
            "lead_notes",
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "note": note,
            },
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "note": note,
            },
        )


# ============================================================================
# STEP 41 — LEAD FOLLOWUPS
# ============================================================================

def seed_lead_followups(db, md):

    print_step(
        "[41] CRM: Lead Follow-ups"
    )

    followups = [
        (
            1,
            "email",
            True,
            "Introductory response sent.",
        ),
        (
            2,
            "whatsapp",
            True,
            "Budget and requirements confirmed.",
        ),
        (
            3,
            "phone",
            False,
            "Follow-up scheduled for proposal approval.",
        ),
        (
            4,
            "email",
            False,
            "Waiting for technical confirmation.",
        ),
    ]

    for (
        lead_no,
        channel,
        completed,
        outcome,
    ) in followups:

        assert_ref(
            "lead",
            lead_no,
        )

        scheduled = (
            utcnow()
            + timedelta(days=lead_no)
        )

        insert_or_get(
            db,
            md,
            "lead_followups",
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "scheduled_at": scheduled,
                "channel": channel,
                "completed": completed,
                "outcome": outcome,
            },
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "scheduled_at": scheduled,
            },
        )


# ============================================================================
# STEP 42 — LEAD STATUS HISTORY
# ============================================================================

def seed_lead_status_history(db, md):

    print_step(
        "[42] CRM: Lead Status History"
    )

    history = [
        (
            1,
            None,
            "NEW",
        ),
        (
            2,
            "NEW",
            "CONTACTED",
        ),
        (
            3,
            "CONTACTED",
            "QUALIFIED",
        ),
        (
            4,
            "QUALIFIED",
            "PROPOSAL_SENT",
        ),
    ]

    for (
        lead_no,
        from_status,
        to_status,
    ) in history:

        assert_ref(
            "lead",
            lead_no,
        )

        insert_or_get(
            db,
            md,
            "lead_status_history",
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "from_status": from_status,
                "to_status": to_status,
            },
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "to_status": to_status,
            },
        )


# ============================================================================
# STEP 43 — COMMUNICATION LOGS
# ============================================================================

def seed_communication_logs(db, md):

    print_step(
        "[43] CRM: Communication Logs"
    )

    communications = [
        (
            1,
            "customer1@example.com",
            "email",
            "outbound",
            "Website enquiry received",
            (
                "Thank you. We will review your "
                "website requirements."
            ),
            "sent",
        ),
        (
            2,
            "customer2@example.com",
            "whatsapp",
            "outbound",
            "E-Commerce requirements",
            (
                "We have received the e-commerce requirements."
            ),
            "sent",
        ),
        (
            3,
            "owner@example.com",
            "phone",
            "outbound",
            "CRM proposal follow-up",
            (
                "Discussed CRM proposal "
                "and implementation scope."
            ),
            "completed",
        ),
        (
            4,
            "founder@example.com",
            "email",
            "outbound",
            "API proposal",
            (
                "Technical API proposal "
                "is ready for review."
            ),
            "sent",
        ),
    ]

    for (
        lead_no,
        email,
        channel,
        direction,
        subject,
        body,
        status,
    ) in communications:

        assert_ref(
            "lead",
            lead_no,
        )

        assert_ref(
            "customer",
            email,
        )

        insert_or_get(
            db,
            md,
            "communication_logs",
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "customer_id": ref(
                    "customer",
                    email,
                ),
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "channel": channel,
                "direction": direction,
                "subject": subject,
                "body": body,
                "status": status,
            },
            {
                "lead_id": ref(
                    "lead",
                    lead_no,
                ),
                "subject": subject,
            },
        )


# ============================================================================
# STEP 44 — AUDIT LOGS
# ============================================================================

def seed_audit_logs(db, md):

    print_step(
        "[44] SYSTEM: Audit Logs"
    )

    audit_rows = [
        (
            "CREATE",
            "services",
            "1",
            None,
            {
                "name": "Website Development"
            },
        ),
        (
            "UPDATE",
            "offers",
            "1",
            {
                "is_active": False
            },
            {
                "is_active": True
            },
        ),
        (
            "CREATE",
            "inquiries",
            "1",
            None,
            {
                "source": "website"
            },
        ),
        (
            "UPDATE",
            "leads",
            "2",
            {
                "status": "NEW"
            },
            {
                "status": "QUALIFIED"
            },
        ),
    ]

    for (
        action,
        module,
        record_id,
        old_value,
        new_value,
    ) in audit_rows:

        insert_or_get(
            db,
            md,
            "audit_logs",
            {
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "action": action,
                "module": module,
                "record_id": record_id,
                "old_value": old_value,
                "new_value": new_value,
                "ip_address": "192.168.10.1",
            },
            {
                "action": action,
                "module": module,
                "record_id": record_id,
            },
        )


# ============================================================================
# STEP 45 — NOTIFICATIONS
# ============================================================================

def seed_notifications(db, md):

    print_step(
        "[45] SYSTEM: Notifications"
    )

    notifications = [
        (
            "New inquiry",
            "A new website inquiry is waiting for review.",
            "/admin/inquiries",
            False,
        ),
        (
            "Lead follow-up",
            "A follow-up is scheduled for today.",
            "/admin/leads",
            False,
        ),
        (
            "Payment received",
            "Demo payment transaction was marked successful.",
            "/admin/payments",
            True,
        ),
    ]

    for (
        title,
        body,
        link,
        is_read,
    ) in notifications:

        insert_or_get(
            db,
            md,
            "notifications",
            {
                "admin_id": ref(
                    "admin",
                    ADMIN_EMAIL,
                ),
                "title": title,
                "body": body,
                "link_url": link,
                "is_read": is_read,
            },
            {
                "title": title,
            },
        )


# ============================================================================
# STEP 46 — COUPON USAGE MAPPING
# ============================================================================

def seed_coupon_usages(db, md):

    print_step(
        "[46] MAPPING: Coupon Usage"
    )

    coupon_t = table(
        md,
        "coupons",
    )

    order_t = table(
        md,
        "orders",
    )

    coupon_row = existing_row(
        db,
        coupon_t,
        {
            "code": "WELCOME10",
        },
    )

    order_row = existing_row(
        db,
        order_t,
        {
            "order_number": "SS-DEMO-0002",
        },
    )

    if not coupon_row:
        raise RuntimeError(
            "Coupon WELCOME10 was not found."
        )

    if not order_row:
        raise RuntimeError(
            "Order SS-DEMO-0002 was not found."
        )

    assert_ref(
        "customer",
        "customer2@example.com",
    )

    coupon_usage_t = table(
        md,
        "coupon_usages",
    )

    insert_or_get(
        db,
        md,
        "coupon_usages",
        {
            "coupon_id": coupon_row[
                pk_name(coupon_t)
            ],
            "order_id": order_row[
                pk_name(order_t)
            ],
            "customer_id": resolve(
                ref(
                    "customer",
                    "customer2@example.com",
                )
            ),
        },
        {
            "coupon_id": coupon_row[
                pk_name(coupon_t)
            ],
            "order_id": order_row[
                pk_name(order_t)
            ],
        },
    )


# ============================================================================
# STEP 47 — TOKEN USAGE
# ============================================================================

def seed_token_usage_logs(db, md):

    print_step(
        "[47] MAPPING: Token Usage"
    )

    wallet_t = table(
        md,
        "customer_wallets",
    )

    token_t = table(
        md,
        "service_tokens",
    )

    token_rows = (
        db.execute(
            select(token_t)
            .order_by(
                token_t.c[
                    pk_name(token_t)
                ]
            )
        )
        .mappings()
        .all()
    )

    if not token_rows:
        raise RuntimeError(
            "No service tokens found for token usage seed."
        )

    emails = [
        "customer1@example.com",
        "customer2@example.com",
        "owner@example.com",
    ]

    for index, email in enumerate(
        emails,
        1,
    ):

        assert_ref(
            "customer",
            email,
        )

        wallet = existing_row(
            db,
            wallet_t,
            {
                "customer_id": resolve(
                    ref(
                        "customer",
                        email,
                    )
                ),
            },
        )

        if not wallet:
            raise RuntimeError(
                f"Customer wallet not found: {email}"
            )

        token = token_rows[
            (index - 1)
            % len(token_rows)
        ]

        change_amount = -index * 10
        balance_after = 100 + change_amount

        insert_or_get(
            db,
            md,
            "token_usage_logs",
            {
                "wallet_id": wallet[
                    pk_name(wallet_t)
                ],
                "service_token_id": token[
                    pk_name(token_t)
                ],
                "admin_id": resolve(
                    ref(
                        "admin",
                        ADMIN_EMAIL,
                    )
                ),
                "change_amount": change_amount,
                "reason": "Demo service usage",
                "balance_after": balance_after,
            },
            {
                "wallet_id": wallet[
                    pk_name(wallet_t)
                ],
                "service_token_id": token[
                    pk_name(token_t)
                ],
                "change_amount": change_amount,
            },
        )


# ============================================================================
# STEP 48 — PAYMENT TRANSACTION MAPPING
# ============================================================================

def seed_payment_transactions(db, md):

    print_step(
        "[48] MAPPING: Payment Transactions"
    )

    payment_t = table(
        md,
        "payments",
    )

    payment_transaction_t = table(
        md,
        "payment_transactions",
    )

    payment_rows = (
        db.execute(
            select(payment_t)
            .order_by(
                payment_t.c[
                    pk_name(payment_t)
                ]
            )
        )
        .mappings()
        .all()
    )

    if not payment_rows:
        print(
            "  No payment rows found; skipping "
            "payment transactions."
        )
        return

    for index, payment in enumerate(
        payment_rows,
        1,
    ):

        payment_id = payment[
            pk_name(payment_t)
        ]

        gateway_reference = (
            payment.get(
                "gateway_payment_id"
            )
            or f"DEMO-TXN-{index}"
        )

        insert_or_get(
            db,
            md,
            "payment_transactions",
            {
                "payment_id": payment_id,
                "event_type": "payment.updated",
                "gateway_reference": gateway_reference,
                "raw_response_summary": (
                    "Demo gateway response recorded by seed."
                ),
            },
            {
                "payment_id": payment_id,
                "event_type": "payment.updated",
            },
        )


# ============================================================================
# VALIDATION
# ============================================================================

def validate_required_data(
    db,
    md,
):
    """
    Validate important master and business tables.

    We intentionally do NOT require every application table to contain
    rows because some operational/log tables may legitimately remain empty.
    """

    print_step(
        "[49] VALIDATION: Required Master Data"
    )

    required_populated_tables = [
        "permissions",
        "roles",
        "admins",
        "service_categories",
        "services",
        "technologies",
        "pages",
        "blog_categories",
        "blog_tags",
        "users",
        "customers",
        "service_packages",
        "service_tokens",
        "offers",
        "coupons",
        "subscription_plans",
    ]

    failed = []

    counts: dict[str, int] = {}

    for name in required_populated_tables:

        if name not in md.tables:
            failed.append(
                f"{name}: table missing"
            )
            continue

        t = md.tables[name]

        count = db.execute(
            select(t)
        ).fetchall()

        total = len(count)

        counts[name] = total

        if total == 0:
            failed.append(
                f"{name}: 0 rows"
            )

    for name in sorted(counts):

        print(
            f"  {name:35} "
            f"{counts[name]:>6}"
        )

    if failed:

        raise RuntimeError(
            "Required master-data validation failed:\n  - "
            + "\n  - ".join(failed)
        )

    print(
        "\n  ✓ Required master data is populated."
    )

    return counts


def validate_application_tables(
    db,
    md,
):
    """
    Print counts for every application table.

    alembic_version is excluded.

    Empty operational tables are reported but do not automatically
    fail the seed.
    """

    print_step(
        "[50] VALIDATION: All Application Tables"
    )

    inspector = inspect(engine)

    application_tables = [
        name
        for name in inspector.get_table_names()
        if name != "alembic_version"
    ]

    counts: dict[str, int] = {}

    empty: list[str] = []

    for name in application_tables:

        if name not in md.tables:
            continue

        t = md.tables[name]

        total = len(
            db.execute(
                select(t)
            ).fetchall()
        )

        counts[name] = total

        if total == 0:
            empty.append(name)

    print("\nTABLE COUNTS")
    print("-" * 65)

    for name in sorted(counts):

        print(
            f"{name:40} "
            f"{counts[name]:>8}"
        )

    if empty:

        print(
            "\nNOTE:"
        )

        print(
            "The following application tables are empty. "
            "This is not treated as a failure because they may "
            "be operational tables that do not require demo data:"
        )

        for name in sorted(empty):

            print(
                f"  - {name}"
            )

    else:

        print(
            "\n✓ Every application table contains at least one row."
        )

    return counts


def validate_refs():
    """
    Validate the in-memory master reference registry.
    """

    print_step(
        "[51] VALIDATION: Seed References"
    )

    required_refs = [
        ("permission", "services.manage"),
        ("permission", "crm.view"),
        ("role", "SUPER_ADMIN"),
        ("admin", ADMIN_EMAIL),

        ("category", "digital-products"),
        ("category", "applications"),
        ("category", "infrastructure"),
        ("category", "business-solutions"),

        ("service", "website-development"),
        ("service", "e-commerce"),
        ("service", "admin-panel"),
        ("service", "rest-api"),
        ("service", "mobile-application"),
        ("service", "crm"),
        ("service", "hosting-deployment"),
        ("service", "automation-integration"),

        ("technology", "React"),
        ("technology", "FastAPI"),
        ("technology", "Python"),
        ("technology", "MySQL"),

        ("page", "home"),
        ("page", "services"),
        ("page", "pricing"),
        ("page", "contact"),

        ("blog_category", "web-development"),
        ("blog_tag", "React"),

        ("user", "customer1@example.com"),
        ("customer", "customer1@example.com"),

        ("plan", "Website Care Monthly"),
        ("plan", "CRM Monthly"),
    ]

    for kind, key in required_refs:

        assert_ref(
            kind,
            key,
        )

    print(
        f"  ✓ Valid references checked: "
        f"{len(required_refs)}"
    )


# ============================================================================
# REQUIRED TABLES
# ============================================================================

REQUIRED_TABLES = [
    # Authentication
    "permissions",
    "roles",
    "role_permissions",
    "admins",

    # Services
    "service_categories",
    "services",
    "technologies",
    "service_technologies",

    # Website
    "pages",
    "page_sections",
    "banners",
    "announcements",
    "seo_meta",
    "settings",
    "social_links",
    "redirects",

    # Projects/content
    "projects",
    "team_members",
    "testimonials",

    # Blog
    "blog_categories",
    "blog_tags",
    "blogs",
    "blog_tag_map",

    # Catalog
    "service_packages",
    "service_features",
    "faqs",
    "service_tokens",
    "offers",
    "coupons",

    # Users/CRM
    "users",
    "customers",
    "inquiries",
    "leads",
    "customer_wallets",

    # Analytics
    "visitors",
    "visitor_sessions",
    "analytics_events",
    "page_views",

    # Sales
    "subscription_plans",
    "orders",
    "payments",
    "invoices",
    "subscriptions",
    "subscription_items",

    # CRM history
    "lead_notes",
    "lead_followups",
    "lead_status_history",
    "communication_logs",

    # System
    "audit_logs",
    "notifications",

    # Financial mappings
    "coupon_usages",
    "token_usage_logs",
    "payment_transactions",
]


# ============================================================================
# MAIN SEED
# ============================================================================

def seed():

    print("=" * 75)
    print("SS PLATFORM DATABASE SEED")
    print("=" * 75)

    print(
        "\nDatabase engine:"
    )

    print(
        f"  {engine.url}"
    )

    # ------------------------------------------------------------------------
    # CREATE TABLES
    # ------------------------------------------------------------------------

    print(
        "\nCreating missing SQLAlchemy tables..."
    )

    # Models have already been imported above.
    #
    # create_all:
    # - creates missing tables
    # - does not delete existing tables
    # - does not alter existing columns
    # - does not touch alembic_version
    Base.metadata.create_all(
        bind=engine
    )

    print(
        "✓ Database tables checked."
    )

    # ------------------------------------------------------------------------
    # REFLECT ACTUAL DATABASE
    # ------------------------------------------------------------------------

    print(
        "\nReading actual database schema..."
    )

    md = reflect_all()

    print(
        f"✓ Reflected {len(md.tables)} database tables."
    )

    # ------------------------------------------------------------------------
    # CHECK REQUIRED TABLES
    # ------------------------------------------------------------------------

    require_tables(
        md,
        REQUIRED_TABLES,
    )

    print(
        "✓ Required application tables found."
    )

    # ------------------------------------------------------------------------
    # CREATE ONE DATABASE SESSION
    # ------------------------------------------------------------------------

    db = SessionLocal()

    try:

        # ====================================================================
        # MASTER DATA
        # ====================================================================

        print_step(
            "MASTER DATA SEEDING"
        )

        # Authentication masters
        seed_permissions(
            db,
            md,
        )

        seed_roles(
            db,
            md,
        )

        seed_admin(
            db,
            md,
        )

        # Service masters
        seed_service_categories(
            db,
            md,
        )

        seed_services(
            db,
            md,
        )

        seed_technologies(
            db,
            md,
        )

        # Website masters
        seed_pages(
            db,
            md,
        )

        # Blog masters
        seed_blog_categories(
            db,
            md,
        )

        seed_blog_tags(
            db,
            md,
        )

        # Customer masters
        seed_users(
            db,
            md,
        )

        seed_customers(
            db,
            md,
        )

        # Catalog masters
        seed_service_packages(
            db,
            md,
        )

        seed_service_features(
            db,
            md,
        )

        seed_faqs(
            db,
            md,
        )

        seed_service_tokens(
            db,
            md,
        )

        seed_offers(
            db,
            md,
        )

        seed_coupons(
            db,
            md,
        )

        # Subscription master
        seed_subscription_plans(
            db,
            md,
        )

        # ====================================================================
        # MAPPINGS
        # ====================================================================

        print_step(
            "MASTER MAPPING SEEDING"
        )

        seed_role_permissions(
            db,
            md,
        )

        seed_service_technology_mappings(
            db,
            md,
        )

        # ====================================================================
        # WEBSITE CONTENT
        # ====================================================================

        print_step(
            "WEBSITE CONTENT SEEDING"
        )

        seed_page_sections(
            db,
            md,
        )

        seed_banners(
            db,
            md,
        )

        seed_announcements(
            db,
            md,
        )

        seed_seo_settings_social(
            db,
            md,
        )

        seed_projects_team_testimonials(
            db,
            md,
        )

        # ====================================================================
        # BLOG
        # ====================================================================

        print_step(
            "BLOG SEEDING"
        )

        seed_blogs(
            db,
            md,
        )

        seed_blog_tag_mappings(
            db,
            md,
        )

        # ====================================================================
        # CRM / BUSINESS
        # ====================================================================

        print_step(
            "CRM / BUSINESS SEEDING"
        )

        seed_inquiries(
            db,
            md,
        )

        seed_leads(
            db,
            md,
        )

        seed_customer_wallets(
            db,
            md,
        )

        # ====================================================================
        # ANALYTICS
        # ====================================================================

        print_step(
            "ANALYTICS SEEDING"
        )

        seed_visitors(
            db,
            md,
        )

        seed_visitor_sessions(
            db,
            md,
        )

        seed_analytics_events(
            db,
            md,
        )

        seed_page_views(
            db,
            md,
        )

        # ====================================================================
        # SALES
        # ====================================================================

        print_step(
            "SALES SEEDING"
        )

        seed_orders(
            db,
            md,
        )

        seed_payments(
            db,
            md,
        )

        seed_invoices(
            db,
            md,
        )

        seed_subscriptions(
            db,
            md,
        )

        seed_subscription_items(
            db,
            md,
        )

        # ====================================================================
        # CRM HISTORY
        # ====================================================================

        print_step(
            "CRM HISTORY / SYSTEM LOG SEEDING"
        )

        seed_lead_notes(
            db,
            md,
        )

        seed_lead_followups(
            db,
            md,
        )

        seed_lead_status_history(
            db,
            md,
        )

        seed_communication_logs(
            db,
            md,
        )

        seed_audit_logs(
            db,
            md,
        )

        seed_notifications(
            db,
            md,
        )

        # ====================================================================
        # FINAL FINANCIAL MAPPINGS
        # ====================================================================

        print_step(
            "FINAL FINANCIAL MAPPINGS"
        )

        seed_coupon_usages(
            db,
            md,
        )

        seed_token_usage_logs(
            db,
            md,
        )

        seed_payment_transactions(
            db,
            md,
        )

        # ====================================================================
        # REFERENCE VALIDATION
        # ====================================================================

        validate_refs()

        # ====================================================================
        # COMMIT ONLY ONCE
        # ====================================================================

        print_step(
            "COMMITTING COMPLETE TRANSACTION"
        )

        print(
            "  No individual commit has been performed."
        )

        print(
            "  All seed operations are inside one transaction."
        )

        db.commit()

        print(
            "  ✓ Transaction committed successfully."
        )

        # ====================================================================
        # DATABASE VALIDATION
        # ====================================================================

        validate_required_data(
            db,
            md,
        )

        counts = validate_application_tables(
            db,
            md,
        )

        # ====================================================================
        # SUCCESS
        # ====================================================================

        print("\n" + "=" * 75)
        print(
            "DATABASE SEED COMPLETED SUCCESSFULLY"
        )
        print("=" * 75)

        print(
            f"\nApplication tables found : {len(counts)}"
        )

        print(
            f"Admin email              : {ADMIN_EMAIL}"
        )

        print(
            f"Admin password           : {ADMIN_PASSWORD}"
        )

        print(
            "\nIMPORTANT:"
        )

        print(
            "Change the default admin password after first login."
        )

        print(
            "\nAPI     : http://localhost:8000"
        )

        print(
            "Swagger : http://localhost:8000/docs"
        )

        print(
            "\nSeed behavior:"
        )

        print(
            "  ✓ Existing records reused"
        )

        print(
            "  ✓ Existing records never deleted"
        )

        print(
            "  ✓ Master data inserted before mappings"
        )

        print(
            "  ✓ Foreign-key references resolved through REF"
        )

        print(
            "  ✓ One final transaction commit"
        )

        print(
            "  ✓ alembic_version untouched"
        )

        print("=" * 75)

    except Exception as exc:

        # ====================================================================
        # COMPLETE ROLLBACK
        # ====================================================================

        db.rollback()

        print(
            "\n" + "=" * 75
        )

        print(
            "DATABASE SEED FAILED"
        )

        print(
            "=" * 75
        )

        print(
            f"\n{type(exc).__name__}: {exc}"
        )

        print(
            "\n✓ Complete seed transaction rolled back."
        )

        print(
            "✓ No partial seed transaction was committed."
        )

        print("=" * 75)

        raise

    finally:

        db.close()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    seed()
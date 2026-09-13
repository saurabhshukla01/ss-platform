"""
SS Platform Database Seeder

Run:
    python -m app.seed

Creates:
    - Permissions
    - SUPER_ADMIN role
    - Super admin account
    - Service categories

Safe to run multiple times.
"""

from app.core.database import SessionLocal, engine, Base
from app.core.security import hash_password
from app.models.identity import Role, Permission, Admin
from app.models.services import ServiceCategory

# Register all SQLAlchemy models
import app.models  # noqa: F401


PERMISSIONS = [
    "services.manage",
    "crm.view",
    "crm.manage",
    "analytics.view",
    "payments.manage",
    "subscriptions.manage",
    "content.manage",
    "settings.manage",
]


CATEGORIES = [
    (
        "Digital Products",
        "digital-products",
        "Website Development, E-Commerce, Admin Panel, REST API",
    ),
    (
        "Applications",
        "applications",
        "Mobile Application, Custom Software, CRM, HRMS, ERP",
    ),
    (
        "Infrastructure",
        "infrastructure",
        "Hosting, Deployment, SSL, DNS, Cloud, Maintenance",
    ),
    (
        "Business Solutions",
        "business-solutions",
        "Automation, Integration, Reporting, Custom Platforms",
    ),
]


ADMIN_EMAIL = "admin@ssplatform.com"
ADMIN_PASSWORD = "ChangeMe123!"


def seed():
    """
    Run database seed.
    """

    print("=" * 60)
    print("SS PLATFORM DATABASE SEED")
    print("=" * 60)

    # Development convenience.
    # Production should use Alembic migrations.
    print("Creating missing database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # =========================================================
        # 1. PERMISSIONS
        # =========================================================

        print("Seeding permissions...")

        perm_objs = {}

        for code in PERMISSIONS:
            perm = (
                db.query(Permission)
                .filter(Permission.code == code)
                .first()
            )

            if not perm:
                perm = Permission(
                    code=code,
                    description=code.replace(".", " ").title(),
                )

                db.add(perm)
                db.flush()

                print(f"  + Permission: {code}")
            else:
                print(f"  ✓ Permission exists: {code}")

            perm_objs[code] = perm

        # =========================================================
        # 2. SUPER ADMIN ROLE
        # =========================================================

        print("Seeding SUPER_ADMIN role...")

        role = (
            db.query(Role)
            .filter(Role.name == "SUPER_ADMIN")
            .first()
        )

        if not role:
            role = Role(
                name="SUPER_ADMIN",
                description="Full access to SS Platform",
            )

            db.add(role)
            db.flush()

            print("  + SUPER_ADMIN role created")
        else:
            print("  ✓ SUPER_ADMIN role already exists")

        # Assign every permission to SUPER_ADMIN
        role.permissions = list(perm_objs.values())

        # =========================================================
        # 3. SUPER ADMIN ACCOUNT
        # =========================================================

        print("Seeding super admin account...")

        admin = (
            db.query(Admin)
            .filter(Admin.email == ADMIN_EMAIL)
            .first()
        )

        if not admin:
            admin = Admin(
                full_name="Saurabh Shukla",
                email=ADMIN_EMAIL,
                hashed_password=hash_password(ADMIN_PASSWORD),
                is_active=True,
                is_super_admin=True,
                role_id=role.id,
            )

            db.add(admin)
            db.flush()

            print(f"  + Admin created: {ADMIN_EMAIL}")

        else:
            # Keep existing admin synchronized
            admin.full_name = "Saurabh Shukla"
            admin.is_active = True
            admin.is_super_admin = True
            admin.role_id = role.id

            print(f"  ✓ Admin already exists: {ADMIN_EMAIL}")

        # =========================================================
        # 4. SERVICE CATEGORIES
        # =========================================================

        print("Seeding service categories...")

        for name, slug, description in CATEGORIES:

            category = (
                db.query(ServiceCategory)
                .filter(ServiceCategory.slug == slug)
                .first()
            )

            if not category:
                category = ServiceCategory(
                    name=name,
                    slug=slug,
                    description=description,
                )

                db.add(category)

                print(f"  + Category: {name}")

            else:
                # Update existing category
                category.name = name
                category.description = description

                print(f"  ✓ Category exists: {name}")

        # =========================================================
        # COMMIT
        # =========================================================

        db.commit()

        print()
        print("=" * 60)
        print("SEED COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print()
        print("Super Admin Login")
        print("------------------")
        print(f"Email    : {ADMIN_EMAIL}")
        print(f"Password : {ADMIN_PASSWORD}")
        print()
        print("IMPORTANT: Change the default password after first login.")
        print("=" * 60)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()
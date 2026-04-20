"""
Database initialization script.
Run this script to create all database tables.

Usage: python scripts/init_db.py
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, SessionLocal
from database.base import Base


def init_database():
    """Create all database tables."""
    print("Creating database tables...")

    # Import all models to register them with Base
    from backend.models import Cliente, Peca, Servico, OrdemServico, OrdemServicoItem

    # Create all tables
    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


def seed_database():
    """Seed database with initial data (optional)."""
    print("Seeding database with initial data...")

    db = SessionLocal()

    try:
        # Check if already seeded
        from backend.models import Cliente

        existing = db.query(Cliente).first()
        if existing:
            print("Database already seeded, skipping...")
            return

        # Add sample data if needed
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    seed_database()
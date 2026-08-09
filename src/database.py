"""
KaFin-Buddy - Database Stage

Responsibilities:
 - Connect to SQLite database
 - Create database tables
 - Insert reference data
 - Insert transformed transactions
 - Prevent duplicate transactions

This module DOES NOT:
 - Ingest raw files
 - Validate raw data
 - Transform transaction data
 - Generate reports
"""

from pathlib import Path
import sqlite3
from config_loader import load_config

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "processed" / "kafin-buddy.db"

def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a connection to the KaFin-Buddy SQLite database.

    Returns:
     - sqlite3.Connection: Active SQLite database connection.
    """

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def create_tables(connection: sqlite3.Connection) -> None:
    """
    Creates all required KaFin-Buddy database tables.

    Args:
     - connection (sqlite3.Connection): Active SQLite connection.
    """

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            category_group TEXT NOT NULL,
            transaction_type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            transaction_date DATE NOT NULL,
            source_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            notes TEXT,
            created_at DATETIME NOT NULL,

            FOREIGN KEY (source_id)
                REFERENCES sources(source_id),

            FOREIGN KEY (category_id)
                REFERENCES categories(category_id)
        )
    """)

    connection.commit()

def insert_sources(
        connection: sqlite3.Connection,
        sources: dict
) -> None:
    """
    Inserts allowed transaction sources into the sources table.

    Args:
     - connection (sqlite3.Connection): Active SQLite connection.
     - sources (dict): Source configuration.
    """

    cursor = connection.cursor()

    allowed_sources = sources["allowed_sources"]

    for source in allowed_sources:
        cursor.execute(
            """
            INSERT OR IGNORE INTO sources (source_name)
            VALUES (?)
            """,
            (source,)
        )

    connection.commit()

def insert_categories(
        connection: sqlite3.Connection,
        categories: dict
) -> None:
    """
    Inserts transaction categories into the categories table.

    Args:
     - connection (sqlite3.Connection): Active SQLite connection.
     - categories (dict): Category configuration.
    """

    cursor = connection.cursor()

    for category_name, category_config in categories.items():
        cursor.execute(
            """
            INSERT OR IGNORE INTO categories (
                category_name,
                category_group,
                transaction_type
            )
            VALUES (?, ?, ?)
            """,
            (
                category_name,
                category_config["group"],
                category_config["type"]
            )
        )

    connection.commit()

if __name__ == "__main__":
    connection = get_connection()

    print("Database connection successful!")

    create_tables(connection)

    print("Database tables created successfully!")

    sources = load_config("sources.json")
    categories = load_config("categories.json")

    insert_sources(
        connection,
        sources
    )

    insert_categories(
        connection,
        categories
    )

    print("Sources and categories inserted successfully!")

    connection.close()

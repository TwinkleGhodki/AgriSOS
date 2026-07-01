import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "history.db"


def get_connection():
    """Returning an SQLite connection."""
    return sqlite3.connect(DATABASE_PATH)


def initialize_database():
    """Creating the prediction history table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT,
            crop TEXT,
            district TEXT,
            risk_level TEXT,
            risk_score REAL,
            weather TEXT,
            recommendation TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(
    farmer_name,
    crop,
    district,
    risk_level,
    risk_score,
    weather,
    recommendation,
    created_at,
):
    """Saving one prediction to the database."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO prediction_history
        (
            farmer_name,
            crop,
            district,
            risk_level,
            risk_score,
            weather,
            recommendation,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        farmer_name,
        crop,
        district,
        risk_level,
        risk_score,
        weather,
        recommendation,
        created_at
    ))

    conn.commit()
    conn.close()


def get_prediction_history():
    """Returning all predictions (latest first)."""

    conn = get_connection()

    query = """
        SELECT
            farmer_name AS "Farmer Name",
            crop AS "Crop",
            district AS "District",
            risk_level AS "Risk Level",
            printf('%.0f%%', risk_score) AS "Risk Score",
            created_at AS "Prediction Time"
        FROM prediction_history
        ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df


def delete_history():
    """Deleting all prediction history."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM prediction_history")

    conn.commit()
    conn.close()
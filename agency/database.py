import sqlite3
from typing import Any, Dict, List, Optional

DB_PATH = "agency_business.db"


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def setup_database() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT,
            email TEXT,
            status TEXT,
            requirements TEXT,
            website_url TEXT,
            invoice_id TEXT,
            last_note TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_lead(business_name: str, email: str, note: str = "") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (business_name, email, status, requirements, website_url, invoice_id, last_note) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (business_name, email, "lead", "", "", "", note),
    )
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return client_id


def fetch_clients_by_status(status: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE status = ?", (status,))
    rows = cursor.fetchall()
    conn.close()
    return [row_to_client(row) for row in rows]


def find_client_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients WHERE email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    return row_to_client(row) if row else None


def fetch_all_clients() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_client(row) for row in rows]


def update_client_field(client_id: int, field_name: str, value: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE clients SET {field_name} = ? WHERE id = ?", (value, client_id))
    conn.commit()
    conn.close()


def update_status(client_id: int, status: str) -> None:
    update_client_field(client_id, "status", status)


def row_to_client(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row[0],
        "business_name": row[1],
        "email": row[2],
        "status": row[3],
        "requirements": row[4] or "",
        "website_url": row[5] or "",
        "invoice_id": row[6] or "",
        "last_note": row[7] or "",
    }

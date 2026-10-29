"""Datenbankschicht des Budget-Planers (SQLite).

Beträge werden als ganze Cent gespeichert (Integer). So gibt es keine
Rundungsfehler, wie sie bei Fließkommazahlen auftreten können.
"""
import sqlite3
from datetime import datetime

EINNAHME = "einnahme"
AUSGABE = "ausgabe"


class BudgetDatabase:
    def __init__(self, path="budget.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                type        TEXT    NOT NULL CHECK (type IN ('einnahme', 'ausgabe')),
                category    TEXT    NOT NULL,
                amount_cent INTEGER NOT NULL CHECK (amount_cent > 0),
                created_at  TEXT    NOT NULL
            )
            """
        )
        self.conn.commit()

    # --- Create ---
    def add_transaction(self, type_, category, amount_cent):
        """Speichert eine Transaktion und gibt ihre ID zurück."""
        if type_ not in (EINNAHME, AUSGABE):
            raise ValueError("Typ muss 'einnahme' oder 'ausgabe' sein.")
        cursor = self.conn.execute(
            "INSERT INTO transactions (type, category, amount_cent, created_at) VALUES (?, ?, ?, ?)",
            (type_, category, amount_cent, datetime.now().strftime("%Y-%m-%d %H:%M")),
        )
        self.conn.commit()
        return cursor.lastrowid

    # --- Read ---
    def get_all(self):
        return self.conn.execute(
            "SELECT id, type, category, amount_cent, created_at FROM transactions ORDER BY id"
        ).fetchall()

    def get_balance_cent(self):
        row = self.conn.execute(
            """
            SELECT COALESCE(SUM(CASE WHEN type = 'einnahme' THEN amount_cent
                                     ELSE -amount_cent END), 0) AS saldo
            FROM transactions
            """
        ).fetchone()
        return row["saldo"]

    # --- Update ---
    def update_transaction(self, id_, category, amount_cent):
        """Ändert Kategorie und Betrag. Gibt False zurück, wenn die ID nicht existiert."""
        cursor = self.conn.execute(
            "UPDATE transactions SET category = ?, amount_cent = ? WHERE id = ?",
            (category, amount_cent, id_),
        )
        self.conn.commit()
        return cursor.rowcount == 1

    # --- Delete ---
    def delete_transaction(self, id_):
        cursor = self.conn.execute("DELETE FROM transactions WHERE id = ?", (id_,))
        self.conn.commit()
        return cursor.rowcount == 1

    def close(self):
        self.conn.close()

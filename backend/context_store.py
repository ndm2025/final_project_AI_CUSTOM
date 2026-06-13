import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[1] / "data" / "context.db"


def _init_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_context (
            user_id TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            PRIMARY KEY (user_id, key)
        )
    """
    )
    conn.commit()
    conn.close()


_store = None


class ContextStore:
    def __init__(self):
        _init_db()
        self._conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)

    def save(self, user_id, key, value):
        self._conn.execute(
            "INSERT OR REPLACE INTO user_context (user_id, key, value) VALUES (?, ?, ?)",
            (user_id, key, value),
        )
        self._conn.commit()
        return True

    def list_for_user(self, user_id):
        rows = self._conn.execute(
            "SELECT key, value FROM user_context WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [{"key": k, "value": v} for k, v in rows]


def get_store():
    global _store
    if _store is None:
        _store = ContextStore()
    return _store

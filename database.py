from flask import g
import sqlite3

DATABASE = "issues.db"


def dict_factory(cursor, row):
    """
    Turns rows into dictionaries (and corrects boolean values) for easier JSON
    conversion. Plugs into Connection.row_factory.
    """

    BOOLEAN_COLUMNS = {"open"}

    d = {}
    for idx, col in enumerate(cursor.description):
        key = col[0]
        value = bool(row[idx]) if key in BOOLEAN_COLUMNS else row[idx]
        d[key] = value

    return d


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


def init_db():
    db = get_db()
    c = db.cursor()
    c.executescript(
        """
        CREATE TABLE IF NOT EXISTS issue(
            project_id TEXT NOT NULL,
            _id TEXT PRIMARY KEY,
            issue_title TEXT NOT NULL,
            issue_text TEXT NOT NULL,
            created_by TEXT NOT NULL,
            assigned_to TEXT NOT NULL DEFAULT "",
            status_text TEXT NOT NULL DEFAULT "",
            created_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_on DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            open BOOLEAN NOT NULL DEFAULT TRUE
        ) WITHOUT ROWID;

        CREATE UNIQUE INDEX IF NOT EXISTS issue_idx ON issue(project_id, _id);
        CREATE INDEX IF NOT EXISTS issue_time ON issue(project_id, updated_on);
        """
    )
    db.commit()

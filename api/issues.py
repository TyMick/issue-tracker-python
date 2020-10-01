from flask import request
from database import get_db
from datetime import datetime, timezone
import nanoid


def get_issues(project_id):
    pass


def add_new_issue(project_id):
    if (
        not request.form.get("issue_title")
        or not request.form.get("issue_text")
        or not request.form.get("created_by")
    ):
        return "Missing required inputs"

    issue_id = nanoid.generate()

    try:
        db = get_db()
        c = db.cursor()
        c.execute(
            """
            INSERT INTO issue(
                project_id,
                _id,
                issue_title,
                issue_text,
                created_by,
                assigned_to,
                status_text
            ) VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (
                project_id,
                issue_id,
                request.form.get("issue_title", ""),
                request.form.get("issue_text", ""),
                request.form.get("created_by", ""),
                request.form.get("assigned_to", ""),
                request.form.get("status_text", ""),
            ),
        )
        db.commit()

        c.execute(
            """
            SELECT
                _id,
                issue_title,
                issue_text,
                created_by,
                assigned_to,
                status_text,
                strftime("%Y-%m-%dT%H:%M:%SZ", created_on) AS created_on,
                strftime("%Y-%m-%dT%H:%M:%SZ", updated_on) AS updated_on,
                open
            FROM issue
            WHERE project_id == ? AND _id == ?
            """,
            (project_id, issue_id),
        )
        return c.fetchone()

    except:
        return "Database error"


def update_issue(project_id):
    pass


def delete_issue(project_id):
    pass

from flask import request, jsonify
from database import get_db
from datetime import datetime, timezone
import nanoid


def get_issues(project_id):
    query = """
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
        WHERE project_id == ?
        """
    parameters = [project_id]

    if request.args.get("_id"):
        query += " AND _id == ?"
        parameters.append(request.args["_id"])
    if request.args.get("issue_title"):
        query += " AND issue_title == ?"
        parameters.append(request.args["issue_title"])
    if request.args.get("issue_text"):
        query += " AND issue_text == ?"
        parameters.append(request.args["issue_text"])
    if request.args.get("created_by"):
        query += " AND created_by == ?"
        parameters.append(request.args["created_by"])
    if request.args.get("assigned_to"):
        query += " AND assigned_to == ?"
        parameters.append(request.args["assigned_to"])
    if request.args.get("status_text"):
        query += " AND status_text == ?"
        parameters.append(request.args["status_text"])
    if request.args.get("created_on"):
        query += " AND created_on == datetime(?)"
        parameters.append(request.args["created_on"])
    if request.args.get("updated_on"):
        query += " AND updated_on == datetime(?)"
        parameters.append(request.args["updated_on"])
    if request.args.get("open"):
        query += " AND open == ?"
        parameters.append(request.args["open"] == "true")

    query += " ORDER BY updated_on DESC"

    try:
        db = get_db()
        c = db.cursor()
        c.execute(query, tuple(parameters))
        return jsonify(c.fetchall())

    except:
        return "Database error"


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
    issue_id = request.form.get("_id")
    if not issue_id:
        return "No issue _id sent"

    updates = dict(request.form)
    del updates["_id"]
    if len(updates) == 0:
        return "No updated field sent"

    query = "UPDATE issue SET"
    parameters = []

    if updates.get("issue_title"):
        query += " issue_title = ?,"
        parameters.append(updates["issue_title"])
    if updates.get("issue_text"):
        query += " issue_text = ?,"
        parameters.append(updates["issue_text"])
    if updates.get("created_by"):
        query += " created_by = ?,"
        parameters.append(updates["created_by"])
    if updates.get("assigned_to"):
        query += " assigned_to = ?,"
        parameters.append(updates["assigned_to"])
    if updates.get("status_text"):
        query += " status_text = ?,"
        parameters.append(updates["status_text"])
    if updates.get("open"):
        query += " open = ?,"
        parameters.append(updates["open"] == "true")

    query += " created_on = CURRENT_TIMESTAMP WHERE project_id == ? AND _id == ?"
    parameters.append(project_id)
    parameters.append(issue_id)

    try:
        db = get_db()
        c = db.cursor()
        c.execute(query, tuple(parameters))
        db.commit()

        c.execute("SELECT changes() AS rows_updated")
        if c.fetchone()["rows_updated"] > 0:
            return "Successfully updated"
        else:
            return f"_id {issue_id} does not exist"

    except:
        return "Database error"


def delete_issue(project_id):
    pass

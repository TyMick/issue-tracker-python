from flask import Flask, g, render_template
from database import init_db
from api.issues import get_issues, add_new_issue, update_issue, delete_issue

app = Flask("app", static_folder="public", template_folder="views")

with app.app_context():
    init_db()


@app.route("/")
def index():
    return render_template("index.html")


app.add_url_rule("/api/issues/<project_id>", view_func=get_issues, methods=["GET"])
app.add_url_rule("/api/issues/<project_id>", view_func=add_new_issue, methods=["POST"])
app.add_url_rule("/api/issues/<project_id>", view_func=update_issue, methods=["PUT"])
app.add_url_rule("/api/issues/<project_id>", view_func=delete_issue, methods=["DELETE"])


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

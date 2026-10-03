from flask import Flask, render_template, session
import os
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv


from project.routes.app_main import main_bp
from project.routes.books import books_bp
from project.routes.auth import auth_bp
from project.routes.account import account_bp
from project.routes.admin import admin_bp
from project.database.db_member import db_log_event


app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

app.secret_key = os.getenv("FLASK_SECRET_KEY")

app.register_blueprint(main_bp)
app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(account_bp)
app.register_blueprint(admin_bp)

app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

@app.errorhandler(400)
def bad_request(e):
    return render_template("errors/400.html"), 400


@app.errorhandler(404)
def not_found(e):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error(e):
    try:
        db_log_event(session.get("user_id"), f"Unhandled server error: {e}", datetime.now(timezone.utc))
    except Exception:
        pass

    return render_template("errors/500.html"), 500

if __name__ == "__main__":
    app.run(debug=True)
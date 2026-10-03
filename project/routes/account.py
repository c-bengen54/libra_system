from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from project.database.db_member import db_find, db_log_event, db_update_member
from project.database.db_book import db_get_book_by, db_get_reservation
from functools import wraps
from datetime import datetime, timezone
import bcrypt

account_bp = Blueprint(
    "account",
    __name__,
    url_prefix="/account"
)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped


@account_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("user/dashboard.html")

@account_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":

        action = request.form.get("action")
        
        if action == "profile":
            field = request.form["field"]

            if field not in ("first_name", "last_name", "email"):
                abort(400)

            new_value = request.form["value"].strip()
            db_update_member(field, new_value, session["user_id"])
            session[field] = new_value

            db_log_event(session["user_id"], f"Updated {field}.", datetime.now(timezone.utc))
            flash("Your information was updated.", "success")

        elif action == "password":
            current_password = request.form["current_password"].encode("utf-8")
            new_password = request.form["new_password"]

            user = db_find("users", "user_id", session["user_id"])
            stored_hash = bytes.fromhex(user[6][2:])

            if not bcrypt.checkpw(current_password, stored_hash):
                flash("Current password is incorrect.", "error")
                return redirect(url_for("account.settings"))

            new_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).strip()
            db_update_member("password_hash", new_hash, session["user_id"])

            db_log_event(session["user_id"], "Changed password.", datetime.now(timezone.utc))
            flash("Password updated.", "success")

        else:
            abort(400)

        return redirect(url_for("account.settings"))

    member = db_find("users", "user_id", session["user_id"])
    return render_template("user/settings.html", member=member)
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    current_app,
)
from models import User
from sqlalchemy import func

admin_auth_bp = Blueprint(
    "admin_auth", __name__, url_prefix="/admin", template_folder="../templates"
)


@admin_auth_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_logged_in") and session.get("is_admin_user"):
        return redirect(url_for("admin_bp.index"))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter(func.lower(User.email) == func.lower(email)).first()
        if user and user.check_password(password) and user.is_admin:
            session.clear()
            session["admin_logged_in"] = True
            session["admin_user_id"] = user.user_id
            session["admin_username"] = user.username
            session["is_admin_user"] = True
            current_app.logger.info(
                f"Admin user '{user.username}' logged in successfully."
            )
            next_url = request.args.get("next")
            return redirect(next_url or url_for("admin_bp.index"))
        else:
            current_app.logger.warning(f"Failed admin login attempt for email: {email}")
            flash("Email atau password salah, atau Anda bukan admin.", "danger")
    return render_template("admin_login.html", title="Admin Login")


@admin_auth_bp.route("/logout")
def admin_logout():
    admin_username = session.get("admin_username", "Admin")
    session.clear()
    flash(f"Anda ({admin_username}) telah berhasil logout dari sesi admin.", "success")
    current_app.logger.info(f"Admin user '{admin_username}' logged out.")
    return redirect(url_for("admin_auth.admin_login"))

from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import query_db


auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please log in as admin.", "warning")
            return redirect(url_for("auth.admin_login"))
        return view(*args, **kwargs)

    return wrapped_view


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not full_name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html")

        existing_user = query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
        if existing_user:
            flash("Email already registered.", "danger")
            return render_template("register.html")

        password_hash = generate_password_hash(password)
        query_db(
            "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
            (full_name, email, password_hash),
            commit=True,
        )
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = query_db("SELECT * FROM users WHERE email = %s", (email,), one=True)

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("destinations.index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", admin_mode=False)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("destinations.index"))


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form.get("password", "")
        admin = query_db("SELECT * FROM admins WHERE username = %s", (username,), one=True)

        if admin and check_password_hash(admin["password_hash"], password):
            session.clear()
            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["username"]
            flash("Admin login successful.", "success")
            return redirect(url_for("auth.admin_dashboard"))

        flash("Invalid admin credentials.", "danger")

    return render_template("login.html", admin_mode=True)


@auth_bp.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    stats = {
        "users": query_db("SELECT COUNT(*) AS count FROM users", one=True)["count"],
        "destinations": query_db("SELECT COUNT(*) AS count FROM destinations", one=True)["count"],
        "bookings": query_db("SELECT COUNT(*) AS count FROM bookings", one=True)["count"],
        "pending": query_db("SELECT COUNT(*) AS count FROM bookings WHERE status = 'Pending'", one=True)["count"],
    }
    recent_bookings = query_db(
        """
        SELECT b.*, u.full_name, d.name AS destination_name
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN destinations d ON b.destination_id = d.id
        ORDER BY b.created_at DESC
        LIMIT 10
        """
    )
    return render_template("admin.html", stats=stats, recent_bookings=recent_bookings)


@auth_bp.route("/dashboard")
@login_required
def dashboard():
    bookings = query_db(
        """
        SELECT b.*, d.name AS destination_name
        FROM bookings b
        JOIN destinations d ON b.destination_id = d.id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
        LIMIT 5
        """,
        (session["user_id"],),
    )
    booking_count = query_db(
        "SELECT COUNT(*) AS count FROM bookings WHERE user_id = %s",
        (session["user_id"],),
        one=True,
    )["count"]
    return render_template("dashboard.html", bookings=bookings, booking_count=booking_count)


@auth_bp.route("/admin/users")
@admin_required
def admin_users():
    users = query_db(
        "SELECT id, full_name, email, created_at FROM users ORDER BY created_at DESC"
    )
    return render_template("admin_users.html", users=users)


@auth_bp.route("/admin/bookings")
@admin_required
def admin_bookings():
    bookings = query_db(
        """
        SELECT b.*, u.full_name, u.email, d.name AS destination_name
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN destinations d ON b.destination_id = d.id
        ORDER BY b.created_at DESC
        """
    )
    return render_template("admin_bookings.html", bookings=bookings)


@auth_bp.route("/admin/destinations")
@admin_required
def admin_destinations():
    destinations = query_db("SELECT * FROM destinations ORDER BY created_at DESC")
    return render_template("admin_destinations.html", destinations=destinations)


@auth_bp.route("/profile")
@login_required
def profile():
    user = query_db("SELECT id, full_name, email, created_at FROM users WHERE id = %s", (session["user_id"],), one=True)
    booking_count = query_db("SELECT COUNT(*) AS count FROM bookings WHERE user_id = %s", (session["user_id"],), one=True)["count"]
    return render_template("profile.html", user=user, booking_count=booking_count)

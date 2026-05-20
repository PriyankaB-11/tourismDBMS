import os
from uuid import uuid4

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from db import query_db
from routes.auth import admin_required


destinations_bp = Blueprint("destinations", __name__)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@destinations_bp.route("/destinations")
def index():
    search = request.args.get("q", "").strip()
    page = max(int(request.args.get("page", 1)), 1)
    per_page = 6
    offset = (page - 1) * per_page

    base_query = "SELECT * FROM destinations"
    params = []
    if search:
        base_query += " WHERE name LIKE %s OR location LIKE %s OR description LIKE %s"
        like_term = f"%{search}%"
        params.extend([like_term, like_term, like_term])

    total = query_db(f"SELECT COUNT(*) AS count FROM ({base_query}) AS filtered", tuple(params), one=True)["count"]
    destinations = query_db(
        f"{base_query} ORDER BY created_at DESC LIMIT %s OFFSET %s",
        tuple(params + [per_page, offset]),
    )
    total_pages = max((total + per_page - 1) // per_page, 1)

    return render_template(
        "index.html",
        destinations=destinations,
        search=search,
        page=page,
        total_pages=total_pages,
    )


@destinations_bp.route("/destinations/<int:destination_id>")
def destination_detail(destination_id):
    destination = query_db("SELECT * FROM destinations WHERE id = %s", (destination_id,), one=True)
    if not destination:
        flash("Destination not found.", "danger")
        return redirect(url_for("destinations.index"))
    return render_template("destination_detail.html", destination=destination)


@destinations_bp.route("/admin/destinations/add", methods=["GET", "POST"])
@admin_required
def add_destination():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0").strip()
        available_slots = request.form.get("available_slots", "0").strip()
        image_file = request.files.get("image")
        image_path = None

        if image_file and image_file.filename:
            if not allowed_file(image_file.filename):
                flash("Invalid image format.", "danger")
                return redirect(request.url)
            filename = secure_filename(image_file.filename)
            filename = f"{uuid4().hex}_{filename}"
            image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)
            image_path = f"images/uploads/{filename}"

        if not name or not location or not description:
            flash("Name, location, and description are required.", "danger")
            return redirect(request.url)

        query_db(
            """
            INSERT INTO destinations (name, location, description, price, image_path, available_slots)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, location, description, price, image_path, available_slots),
            commit=True,
        )
        flash("Destination added successfully.", "success")
        return redirect(url_for("auth.admin_destinations"))

    return render_template("destination_form.html", destination=None)


@destinations_bp.route("/admin/destinations/<int:destination_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_destination(destination_id):
    destination = query_db("SELECT * FROM destinations WHERE id = %s", (destination_id,), one=True)
    if not destination:
        flash("Destination not found.", "danger")
        return redirect(url_for("auth.admin_destinations"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0").strip()
        available_slots = request.form.get("available_slots", "0").strip()
        image_file = request.files.get("image")
        image_path = destination["image_path"]

        if image_file and image_file.filename:
            if not allowed_file(image_file.filename):
                flash("Invalid image format.", "danger")
                return redirect(request.url)
            filename = secure_filename(image_file.filename)
            filename = f"{uuid4().hex}_{filename}"
            saved_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            image_file.save(saved_path)
            image_path = f"images/uploads/{filename}"

        query_db(
            """
            UPDATE destinations
            SET name = %s, location = %s, description = %s, price = %s, image_path = %s, available_slots = %s
            WHERE id = %s
            """,
            (name, location, description, price, image_path, available_slots, destination_id),
            commit=True,
        )
        flash("Destination updated successfully.", "success")
        return redirect(url_for("auth.admin_destinations"))

    return render_template("destination_form.html", destination=destination)


@destinations_bp.route("/admin/destinations/<int:destination_id>/delete", methods=["POST"])
@admin_required
def delete_destination(destination_id):
    query_db("DELETE FROM destinations WHERE id = %s", (destination_id,), commit=True)
    flash("Destination deleted successfully.", "success")
    return redirect(url_for("auth.admin_destinations"))

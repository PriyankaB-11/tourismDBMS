from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from db import query_db
from routes.auth import admin_required, login_required


booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/book/<int:destination_id>", methods=["GET", "POST"])
@login_required
def book(destination_id):
    destination = query_db("SELECT * FROM destinations WHERE id = %s", (destination_id,), one=True)
    if not destination:
        flash("Destination not found.", "danger")
        return redirect(url_for("destinations.index"))

    if request.method == "POST":
        travel_date = request.form.get("travel_date", "").strip()
        guests = int(request.form.get("guests", 1))
        notes = request.form.get("notes", "").strip()

        if guests < 1:
            flash("Guests must be at least 1.", "danger")
            return redirect(request.url)

        query_db(
            """
            INSERT INTO bookings (user_id, destination_id, travel_date, guests, notes, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
            """,
            (session["user_id"], destination_id, travel_date, guests, notes),
            commit=True,
        )
        flash("Booking created successfully.", "success")
        return redirect(url_for("booking.confirmation", destination_id=destination_id))

    return render_template("book.html", destination=destination)


@booking_bp.route("/booking-confirmation/<int:destination_id>")
@login_required
def confirmation(destination_id):
    destination = query_db("SELECT * FROM destinations WHERE id = %s", (destination_id,), one=True)
    latest_booking = query_db(
        """
        SELECT * FROM bookings
        WHERE user_id = %s AND destination_id = %s
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (session["user_id"], destination_id),
        one=True,
    )
    return render_template("booking_confirmation.html", destination=destination, booking=latest_booking)


@booking_bp.route("/bookings")
@login_required
def bookings():
    bookings_list = query_db(
        """
        SELECT b.*, d.name AS destination_name, d.location, d.image_path
        FROM bookings b
        JOIN destinations d ON b.destination_id = d.id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
        """,
        (session["user_id"],),
    )
    return render_template("bookings.html", bookings=bookings_list)


@booking_bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = query_db(
        "SELECT * FROM bookings WHERE id = %s AND user_id = %s",
        (booking_id, session["user_id"]),
        one=True,
    )
    if not booking:
        flash("Booking not found.", "danger")
        return redirect(url_for("booking.bookings"))

    query_db("UPDATE bookings SET status = 'Cancelled' WHERE id = %s", (booking_id,), commit=True)
    flash("Booking cancelled.", "success")
    return redirect(url_for("booking.bookings"))


@booking_bp.route("/admin/bookings/<int:booking_id>/status", methods=["POST"])
@admin_required
def update_booking_status(booking_id):
    status = request.form.get("status", "Pending")
    if status not in {"Pending", "Confirmed", "Cancelled", "Completed"}:
        flash("Invalid booking status.", "danger")
        return redirect(url_for("auth.admin_bookings"))

    query_db("UPDATE bookings SET status = %s WHERE id = %s", (status, booking_id), commit=True)
    flash("Booking status updated.", "success")
    return redirect(url_for("auth.admin_bookings"))

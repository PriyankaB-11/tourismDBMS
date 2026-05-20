# Tourism Management System

Simple Flask + MySQL tourism management app with user authentication, destination management, bookings, and an admin panel.

## Features
- User registration, login, logout, and profile
- Password hashing and session management
- Destination listing, search, add, edit, delete
- Booking creation, history, cancellation
- Admin dashboard, users, bookings, destinations
- MySQL schema with sample data
- Bootstrap UI

## Requirements
- Python 3.10+
- MySQL Server
- MySQL Workbench

## Setup
1. Create a MySQL database named `tourism_db`.
2. Run `database/schema.sql` in MySQL Workbench.
3. Update database credentials in `config.py` or set environment variables. By default the app uses `root` with an empty password, which matches many local MySQL installs.
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000`.

## Default demo data
- Admin username: `admin`, password: `admin123`
- Sample users: `aarav@example.com` / `user123` and `meera@example.com` / `user123`
- These credentials are loaded from the SQL seed data after importing `database/schema.sql`.

## Notes
- Image uploads are saved under `static/images/uploads`.
- The app uses parameterized SQL queries through `mysql-connector-python`.
- Database schema includes indexes and check constraints for better DBMS quality.
 
## UI improvements & extra sample data
- Added improved styling and interactive cards (hover, price badge).
- Placeholder images were added under `static/images/uploads` and several extra sample destinations were inserted.
- To add the demo destinations (if you re-created the DB), run:

```bash
python populate_sample.py
```

This script inserts a few ready-to-use destinations with image paths.

## DBMS upgrades
- Added integrity checks in `database/schema.sql`:
   - `price >= 0`
   - `available_slots >= 0`
   - `guests > 0`
- Added indexes in `database/schema.sql` for faster filtering and joins:
   - users: `email`
   - destinations: `name`, `location`
   - bookings: `user_id`, `destination_id`, `status`, `travel_date`
- Added reporting queries in `database/reports.sql`:
   - destination-wise bookings and estimated revenue
   - booking status summary
   - user-wise booking count and estimated spend
   - upcoming bookings list
   - slot pressure overview

To run reports in MySQL Workbench:
1. Open and execute `database/schema.sql` (if not already imported).
2. Open `database/reports.sql`.
3. Execute all statements to get report tables.

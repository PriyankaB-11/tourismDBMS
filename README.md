# Tourism Management System

A simple prototype web application for managing tourism destinations and bookings. Built with Flask (Python) and MySQL, this project demonstrates authentication, destination CRUD, booking flow, a small admin panel, and reporting-ready database schema.

## Quick overview
- Users: register, login, book destinations, view and cancel bookings
- Admin: manage destinations, view users and bookings, update booking status
- Database: MySQL schema with seed data, indexes, and CHECK constraints
- Frontend: Bootstrap-based templates, images served from `static/images/uploads`

## Tech stack
- Python 3.10+
- Flask
- mysql-connector-python (raw parameterized SQL helper in `db.py`)
- Bootstrap, basic JS
- Pillow + requests (helper scripts for image download/resize)

## Repository layout (important files)
- `app.py` — Flask app factory and blueprint registration
- `config.py` — configuration (DB credentials, upload folder)
- `db.py` — connection helpers and `query_db()` wrapper
- `routes/` — `auth.py`, `destinations.py`, `booking.py` (blueprints)
- `templates/`, `static/` — UI templates, CSS, JS, images
- `database/schema.sql` — full DDL and seed data
- `database/reports.sql` — reporting queries
- `populate_sample.py` — script to insert sample destinations
- `download_images.py` — helper to download and resize sample photos
- `fix_image_paths.py` — normalizes Windows backslashes in DB paths

## Prerequisites (local development)
- Install Python 3.10 or newer
- Install MySQL Server (local) and MySQL Workbench (recommended for running SQL files)
- Create a virtual environment for Python

## Step-by-step: Run the prototype after cloning
Follow these commands in a terminal at the project root after cloning this repo.

1) Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # PowerShell
# or on cmd: .\.venv\Scripts\activate.bat
# or on bash: source .venv/bin/activate
```

2) Install Python dependencies

```powershell
pip install -r requirements.txt
```

3) Configure database credentials

- You can either edit `config.py` or set environment variables. `config.py` reads values from environment variables when present. Important variables:
  - `MYSQL_HOST` (default: `localhost`)
  - `MYSQL_USER` (e.g., `root`)
  - `MYSQL_PASSWORD`
  - `MYSQL_DATABASE` (recommended: `tourism_db`)
  - `MYSQL_PORT` (default: `3306`)

Example (PowerShell):

```powershell
$env:MYSQL_USER='root'
$env:MYSQL_PASSWORD='your_mysql_password'
$env:MYSQL_DATABASE='tourism_db'
```

4) Create the database and import schema

- Open MySQL Workbench (or use the `mysql` CLI) and create a database named `tourism_db` (or your chosen name used in step 3).
- In Workbench, open and run `database/schema.sql`. It creates tables (`users`, `admins`, `destinations`, `bookings`), indexes, constraints, and seed data (including demo admin and users).

Command-line alternative (if `mysql` client available):

```powershell
# adjust user/host/port as needed
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS tourism_db;"
mysql -u root -p tourism_db < database/schema.sql
```

5) (Optional) Populate/download images and fix paths

- If you want local photos used by the sample destinations, run:

```powershell
\.venv\Scripts\python.exe download_images.py
```

- If you imported the schema on Windows and image paths show backslashes, normalize them:

```powershell
\.venv\Scripts\python.exe fix_image_paths.py
```

6) (Optional) Re-run sample-populate (idempotent)

```powershell
\.venv\Scripts\python.exe populate_sample.py
```

7) Run the Flask app (development)

```powershell
\.venv\Scripts\python.exe app.py
# or
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Demo credentials (seeded)
- Admin: `admin` / `admin123`
- Sample users included in `database/schema.sql` (see the file for specific emails and passwords)

## Database design summary
- `users` — registered users (id, name, email(unique), password_hash, created_at)
- `admins` — admin accounts
- `destinations` — catalog of trips (id, name, location, price, available_slots, description, image_path)
- `bookings` — bookings made by users (id, user_id FK, destination_id FK, guests, travel_date, status, created_at)

Important DB notes:
- Several CHECK constraints enforce `price >= 0`, `available_slots >= 0`, and `guests > 0`.
- Indexes added for faster lookups (email, name, location, booking status, travel_date).
- The schema is intentionally simple (raw, parameterized SQL). For larger projects consider an ORM (SQLAlchemy) and migrations (Alembic).

## Reports and analysis
- `database/reports.sql` contains a set of read-only SELECT queries useful for demos and grading (destination revenue, booking status summary, user booking totals, upcoming bookings, slot pressure). Run it in Workbench or via script to produce CSV results.

## Troubleshooting
- MySQL access denied: ensure `MYSQL_USER`/`MYSQL_PASSWORD` are correct and the user has privileges for `tourism_db`.
- Images not showing: ensure files exist under `static/images/uploads/` and that `image_path` values in `destinations` use forward slashes (run `fix_image_paths.py` if needed).
- Port in use: change Flask port in `app.py` or stop the conflicting service.

## Developer notes & next steps
- Admin upload UI and server-side bulk image management are optional enhancements.
- Consider adding DB triggers to auto-deduct/restore `available_slots` on booking confirm/cancel for stronger integrity.

## Scripts of interest
- `download_images.py` — downloads remote images, center-crops/resizes, saves to `static/images/uploads/`, and updates DB image paths.
- `populate_sample.py` — inserts sample destinations if not present.
- `fix_image_paths.py` — replace backslashes with forward slashes in `destinations.image_path`.

## Contributing & License
This is a small demo/prototype. You're welcome to fork and extend it. No license file included — treat it as sample code for learning unless you add a license.

---
If you'd like, I can now commit these README changes, create a PR, or push to your configured GitHub remote. Tell me which you'd prefer.

## Rubric mapping & enhancements

This section maps the assessment rubric used for evaluation to the project's artifacts and notes on enhancements made to reach "Excellent" criteria.

- **ER Diagram & Conceptual Design (CO2)**: The schema is defined in `database/schema.sql`. A visual ER diagram and conceptual explanation have been added in `docs/er_diagram.md` (entities, attributes, relationships, and cardinalities).
- **SQL Query Development (CO3)**: Reporting queries are in `database/reports.sql`. Query optimization notes and EXPLAIN guidance are in `docs/query_optimizations.md`. Queries in routes are parameterized and use joins/aggregates where appropriate.
- **Normalization & Schema Design (CO4)**: Schema normalized to 3NF with PK/FK constraints and CHECK constraints. Triggers were added to `database/schema.sql` to enforce `available_slots` accounting and prevent overbooking.
- **Application Integration (Front-end) (CO5)**: Full CRUD and booking flows are implemented in `routes/`. Trigger error handling was added to `routes/booking.py` to present friendly messages when DB constraints prevent an operation. Unit tests for booking status updates and trigger handling are in `tests/test_booking_flow.py`.
- **Requirement Analysis & Documentation (CO1)**: `README.md` provides setup and run instructions. Additional docs (`docs/er_diagram.md`, `docs/query_optimizations.md`, `migrations/README.md`) document requirements, design rationale, and migration guidance.

### How to validate the grading checklist locally

1. Import the schema (includes triggers):

```powershell
mysql -u root -p tourism_db < database/schema.sql
```

2. Run tests (from project root, venv activated):

```powershell
pip install -r requirements.txt
pytest -q
```

3. Start the app and exercise admin booking confirmation and cancellation flows to observe trigger-driven behavior.

If you'd like, I can add CI (GitHub Actions) to run tests and migrations automatically on push.

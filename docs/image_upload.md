Image upload and management

This document explains how images are handled, how to add/replace images, and how to run the helper scripts included in this project.

1) Where images are stored
- Local images live under `static/images/uploads/`.
- `destinations.image_path` stores either a local path (e.g. `images/uploads/goa.jpg`) or a full HTTP(S) URL.

2) Recommended image format
- JPEG, 1200×800 (aspect 3:2) is recommended for destination cards and detail pages.
- Optimized JPEG quality 80–85 balances size and quality.

3) Automatic downloader & seeder
- `download_images.py` (already run): downloads sample images from the web, center-crops and resizes to 1200×800, saves under `static/images/uploads/`, and updates the database `destinations.image_path` fields to local paths.
- `populate_sample.py`: inserts sample destinations if missing and also updates image_path fields for seeded destinations.

Commands (run from project root, with venv active):

```powershell
# activate venv (PowerShell)
& .venv\Scripts\Activate.ps1

# run downloader (downloads + updates DB)
python download_images.py

# run seeder (inserts additional destinations and sets remote URLs)
python populate_sample.py
```

4) Manually adding or replacing an image
- Copy your image file into `static/images/uploads/` (use a descriptive name, e.g. `goa-beach.jpg`).
- Update the DB row for the destination to reference the new path. Example SQL (run in MySQL Workbench):

```sql
USE tourism_db;
UPDATE destinations
SET image_path = 'images/uploads/goa-beach.jpg'
WHERE name = 'Goa Beach Escape';
```

5) Admin upload option (manual for now)
- There is no admin file-upload UI in this scaffold yet. To add a UI, we can implement a small admin form under `/admin/destinations/add` to accept file uploads; ask me if you'd like this.

6) Verify and restart the Flask app
- Static files are served immediately in Flask dev mode. If the server is running, refresh the page.
- To restart the dev server (if needed):

```powershell
# (from project root)
& .venv\Scripts\Activate.ps1
python app.py
```

7) Notes
- If you prefer cloud storage (S3) or CDN, update `image_path` to the CDN URL and the templates will render them directly.
- For mobile optimization, we can generate `srcset` variants (e.g., 600w, 1200w) and update templates to use `srcset` and lazy-loading.

If you'd like, I can now add an admin image upload form and handler that saves files into `static/images/uploads/` and updates the DB automatically.

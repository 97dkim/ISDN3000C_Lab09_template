# ISDN3000C Lab 09 - Guestbook (Flask)

This repository contains a simple Flask guestbook application (lab template) with a small SQLite database, a Dockerfile, and an optional nginx reverse proxy configuration. The README below explains how to set up and run the project locally and with Docker.

## Table of contents

- Project overview
- Requirements
- Quick start (local)
- Initialize the database
- Run with Docker / docker-compose
- nginx reverse-proxy (provided)
- API & web endpoints
- Project structure
- Troubleshooting
- License

## Project overview

The app is a minimal guestbook where visitors can submit short messages (<= 140 chars). It includes:

- A web UI (served from `FlaskApp/templates/index.html`).
- A JSON API endpoint at `/api/messages` to POST messages programmatically.
- A lightweight SQLite database (`database.db`) initialized from `FlaskApp/schema.sql` by `FlaskApp/init_db.py`.

This template is intended for learning and lab use. Secrets and production hardening (secret keys, CORS, rate-limiting, input sanitization beyond basics) are intentionally minimal.

## Requirements

- Python 3.8+ (the Dockerfile uses Python 3.11)
- pip
- Optional: Docker and docker-compose if you want to run in containers

The project's Python dependencies are listed in `requirements.txt`.

## Quick start (local development)

Recommended: create and use a virtual environment.

PowerShell (Windows) example:

```powershell
# create venv
python -m venv .venv
# activate venv (PowerShell)
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

If PowerShell blocks script execution, run as Administrator and set execution policy, or use Command Prompt activation: `.
.venv\Scripts\activate`.

### Initialize the database

The project includes `FlaskApp/init_db.py` which creates `database.db` based on `FlaskApp/schema.sql`.

From the repository root (PowerShell):

```powershell
python FlaskApp\init_db.py
```

After running, you should see `Database initialized successfully.` and a `database.db` file in the working directory (or inside the container if using Docker).

### Run the Flask app

From the repository root with the venv active:

```powershell
# run directly with python
python FlaskApp\app.py

# or run with flask CLI (if FLASK_APP is set)
# $env:FLASK_APP = "FlaskApp.app"; flask run
```

By default, `app.py` uses Flask's built-in server and will listen on `127.0.0.1:5000` (development only). You can open http://127.0.0.1:5000/ in your browser.

## Run with Docker / docker-compose

The repository includes a `Dockerfile` and `docker-compose.yml` to run the Flask app together with an nginx reverse proxy.

Build and run with docker-compose from the repo root:

```powershell
docker-compose up --build -d
```

Behavior:

- The `flask-app` service builds from the `Dockerfile` and runs Flask (exposes port 5000 inside the container).
- The `nginx` service maps host port 80 to the container and forwards traffic to the Flask service according to `nginx/nginx.conf`.

To stop and remove containers:

```powershell
docker-compose down
```

Notes:

- The `docker-compose.yml` mounts `./FlaskApp/database.db` into the container so DB changes persist on the host.
- The Dockerfile runs `init_db.py` during the build to create the DB schema inside the image; after building, the compose mount will preserve the DB on the host.

## nginx reverse-proxy (provided)

An example `nginx/nginx.conf` is included to route requests to the Flask app. `docker-compose.yml` mounts this config into the nginx container. If you run `docker-compose up` you can access the site on http://localhost/ (port 80) and nginx will proxy requests to the Flask container.

## API & web endpoints

- Web UI (GET /): renders the guestbook form and lists messages.
- POST / (form): standard form submission to create a new message.
- POST /api/messages (JSON): accepts JSON payloads to create a message. Example payload:

```json
{
	"name": "Alice",
	"message": "Hello from the API!"
}
```

Response codes:

- 201 Created — message added successfully
- 400 Bad Request — validation error (missing name/message or message too long)
- 500 Internal Server Error — DB error

- GET /health — simple health check (returns 200 and a message)
- GET /about — short about message

## Project structure

Top-level files and folders:

- `FlaskApp/` — Flask app code, templates and DB helpers
	- `app.py` — main app and endpoints
	- `init_db.py` — creates `database.db` using `schema.sql`
	- `schema.sql` — DB schema for messages table
	- `templates/index.html` — web UI template
- `Dockerfile` — image definition for the Flask app
- `docker-compose.yml` — launches Flask + nginx
- `nginx/nginx.conf` — example nginx config
- `requirements.txt` — Python dependencies

## Troubleshooting

- If flask fails to start in your shell when using `flask run`, ensure `FLASK_APP` is set to `FlaskApp.app` or run `python FlaskApp\app.py` directly.
- PowerShell execution policy can block activation of scripts; use Command Prompt to activate a venv if needed, or run PowerShell as Administrator to change policy.
- If you get DB locked errors, ensure no other process has an open connection to `database.db` or delete the file and re-run `init_db.py`.
- When using Docker, if nginx returns 502/504, check that the Flask container is up and listening on port 5000 and that the nginx config points to the correct host/port.



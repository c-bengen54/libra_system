# Library Management System — Flask Application

A web-based Library Management System built with Python, Flask, and PostgreSQL.

This repository contains the web-facing stage of the Library Management System, having transitioned from a terminal-based application into a containerized, publicly deployed browser application.

## Current Status

**Core functionality complete; feature-complete for member and admin workflows.**

The application is fully containerized, runs behind a production WSGI server, and is deployed with a hosted database. Remaining work is centered on library-specific features (search, due dates) rather than infrastructure.

### Remaining Development

* Advanced book search and filtering
* Due dates and overdue tracking
* Member-facing view of currently borrowed books
* Member-facing view of active reservations
* Automated testing

## Implemented Features

* Flask web application, organized into blueprints
* User registration and login with session-based authentication
* Password hashing with `bcrypt`, including self-service password changes
* Time-based one-time passcode (TOTP) system gating administrator registration — compatible with standard authenticator apps (Microsoft/Google Authenticator), no stored access codes in the database
* Administrator dashboard: add books, remove books, look up and update member accounts by username
* Audit logging: authentication events, book checkouts/reservations/returns, administrator actions, and unhandled server errors are all recorded to a persistent `logs` table
* Centralized, styled error pages (400, 404, 500)
* Account settings page for updating profile information and changing passwords
* PostgreSQL database integration via a connection pool (safe for concurrent, multi-user access)
* Book management: checkout, return, reservation, with ISBN-10/13 validation
* Database-backed persistent storage, hosted on Neon (PostgreSQL)
* Containerized with Docker and Docker Compose
* Deployed to production via Render, running under `gunicorn`

## Technologies

* **Python** — application logic
* **Flask** — web application framework
* **PostgreSQL** — persistent database (hosted on [Neon](https://neon.tech))
* **psycopg3** / **psycopg_pool** — database connectivity with connection pooling
* **gunicorn** — production WSGI server
* **Docker** / **Docker Compose** — containerization and local multi-service orchestration
* **bcrypt** — password hashing
* **pyotp** — TOTP generation/verification for administrator registration
* **PL/pgSQL** — database-side functions and validation
* **HTML/CSS** — web interface
* **Jinja2** — Flask templating
* **Render** — application hosting
* **Git/GitHub** — version control

## Application Architecture

```text
Browser
   │
   ▼
Flask Routes / Blueprints
   │
   ▼
Application Logic
   │
   ▼
Database Functions (connection pool)
   │
   ▼
PostgreSQL (Neon)
```

Flask handles HTTP requests and renders the web interface; the database layer handles all communication with PostgreSQL through a pooled connection, so concurrent requests from multiple users don't contend for a single connection.

## Project Structure

```text
library_exercise/
│
├── project/
│   ├── app.py
│   │
│   ├── database/
│   │   ├── db.py              # connection pool
│   │   ├── db_book.py
│   │   └── db_member.py
│   │
│   ├── database_setup/
│   │   ├── sample_data.sql
│   │   └── schema.sql
│   │
│   ├── routes/
│   │   ├── app_main.py
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── account.py
│   │   └── admin.py
│   │
│   ├── templates/
│   │   ├── admin/
│   │   ├── book/
│   │   ├── system/
│   │   ├── user/
│   │   └── errors/
│   │
│   └── static/
│       ├── css/
│       └── images/
│        
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── README.md
└── requirements.txt
```

## Database

The application uses PostgreSQL for persistent storage, hosted on Neon. The database contains tables for:

* Users
* Books
* Borrowed books
* Reservations
* Logs

### Users

Stores registered users and their account information, including authentication data and user type (`member` or `admin`). Passwords are stored as `bcrypt` hashes, never in plaintext.

### Books

Stores library book information and tracks whether each book is currently checked out. ISBN values are validated using a PostgreSQL function and constraint.

### Borrowed Books

Associates members with books they currently have borrowed and records the borrowing time.

### Reservations

Stores reservations made by members for books that are unavailable.

### Logs

Records application events — logins, logouts, registrations, checkouts, returns, reservations, administrator actions, and unhandled server errors — each tied to the responsible user where applicable.

## Authentication

Users can register and log into the application through the Flask web interface. After successful authentication, Flask sessions associate requests with the logged-in user, allowing the application to display user-specific information such as account details and reservation activity.

### Administrator Registration

Administrator access during registration is gated by a TOTP (time-based one-time passcode) check rather than a password stored in the database. A super admin holds the shared secret (configured via an authenticator app or a one-time setup script) and issues the current rotating code to whoever needs to register as a lower-level admin. Because the code is derived algorithmically from a secret and the current time, nothing admin-related is ever persisted to the database — a database compromise alone cannot expose or regenerate valid admin codes.

## ISBN Validation

A PostgreSQL PL/pgSQL function validates ISBN-10 and ISBN-13 values, performing format and checksum validation. A database constraint uses this function to prevent invalid ISBN values from being stored.

## Configuration

The application is configured entirely through environment variables, kept out of version control via `.gitignore`. See `.env.example` for the full list. Required variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (Neon in production) |
| `FLASK_SECRET_KEY` | Signs session cookies |
| `ADMIN_TOTP_SECRET` | Shared TOTP secret for admin registration |
| `COOKIE_SECURE` | Set to `1` in production to require HTTPS for session cookies |

## Running the Application

### With Docker (recommended)

From the project root, with a `.env` file present:

```bash
docker compose up --build
```

This starts both the Flask application (via `gunicorn`) and a local PostgreSQL instance, with the database schema applied automatically on first run. The app is then available at `http://localhost:8000`.

### Without Docker

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

With `.env` configured and a running PostgreSQL instance, start the app as a module (required, due to the project's package structure):

```bash
python -m project.app
```

For a production-style run with multiple workers:

```bash
gunicorn -w 4 -b 0.0.0.0:8000 "project.app:app"
```

## Deployment

The application is deployed to [Render](https://render.com) as a Docker-based web service, with [Neon](https://neon.tech) providing hosted PostgreSQL. Render builds and runs the image directly from the repository's `Dockerfile`; no separate start command is configured. Environment variables (see Configuration above) are set directly in the Render dashboard.

## Legacy Terminal Application

An earlier terminal-based version of this project (`main.py`, `system.py`, `models/`) is present in the project history but is no longer tracked in version control or maintained. All current development targets the Flask web application exclusively.

## Future Goals

* Advanced search and filtering
* Due dates and overdue tracking
* Member-facing views for borrowed books and reservations
* Automated testing

## License

This project is primarily intended as an educational/student project.
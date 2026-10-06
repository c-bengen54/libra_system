# Library Management System — Flask Application

A work-in-progress web-based Library Management System built with Python, Flask, and PostgreSQL.

This repository contains the next stage of the Library Management System, transitioning the project from a terminal-based application into a browser-accessible web application.

The project builds upon the database and application architecture developed in the terminal version while introducing Flask, HTML/CSS, session-based authentication, and a web interface.

## Current Status

**Work in progress.**

The core Flask application, database integration, authentication, and primary library functionality are currently implemented. Several components remain under development before the application can be considered production-ready.

### Remaining Development

* Advanced search systems
* Due dates
* Overdue tracking
* Viewing borrowed books
* Viewing reservations
## Implemented Features

* Flask web application
* Expanded logging
* Custom error handling
* Containerization
* Production deployment/rollout
* Book searching
* User registration
* User login
* Session-based authentication
* Password hashing with `bcrypt`
* PostgreSQL database integration
* Book management
* Book checkout
* Book returns
* Book reservations
* Database-backed persistent storage
* ISBN-10 and ISBN-13 validation
* Database functions and constraints
* HTML/CSS web interface

## Technologies

* **Python** — application logic
* **Flask** — web application framework
* **PostgreSQL** — persistent database
* **psycopg** — Python/PostgreSQL connection
* **bcrypt** — password hashing
* **PL/pgSQL** — database-side functions and validation
* **HTML/CSS** — web interface
* **Jinja2** — Flask templating
* **Git/GitHub** — version control

## Application Architecture

The application is separated into several layers:

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
Database Functions
   │
   ▼
PostgreSQL
```

Flask handles HTTP requests and renders the web interface, while the database layer handles communication with PostgreSQL.

This separation allows the web interface to interact with the same underlying library data without placing database operations directly inside the HTML templates.

## Project Structure

```text
library_exercise/
│
├── database/
│   ├── db.py
│   ├── db_book.py
│   └── db_member.py
│
├── database_setup/
│   ├── sample_data.sql
│   └── schema.sql
│
├── templates/
│   └── ...
│
├── static/
│   └── ...
│
├── routes/
│    ├── auth.py
│    ├── books.py
│    ├── account.py
│    ├── member.py
│    └── admin.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

> The structure is subject to change as development continues.

## Database

The Flask application uses PostgreSQL for persistent storage.

The database currently contains tables for:

* Users
* Books
* Borrowed books
* Reservations
* Logs
* Administrator access

### Users

Stores registered users and their account information, including authentication data and user type.

Passwords are stored as hashes rather than plaintext passwords.

### Books

Stores library book information and tracks whether each book is currently checked out.

ISBN values are validated using a PostgreSQL function.

### Borrowed Books

Associates members with books they currently have borrowed and records the borrowing time.

### Reservations

Stores reservations made by members for books that are unavailable.

### Logs

Provides a database-backed system for recording application events. Additional logging functionality remains under development.

### Administrator Access

The database includes support for administrator access codes.

The intended system uses periodically changing access codes rather than relying solely on a permanent administrator password. Further administrator functionality remains to be implemented.

## Authentication

Users can register and log into the application through the Flask web interface.

After successful authentication, Flask sessions are used to associate requests with the currently logged-in user.

This allows the application to display user-specific information such as:

* Borrowed books
* Reservations
* Account information

Passwords are protected using `bcrypt` hashing.

## ISBN Validation

A PostgreSQL PL/pgSQL function validates ISBN-10 and ISBN-13 values.

The function performs format and checksum validation and is used by a database constraint to prevent invalid ISBN values from being stored.

## Configuration

Database credentials and other sensitive configuration values should not be committed to Git.

The application should be configured through environment variables or an equivalent secure configuration system.

A `.env` file may be used for local development when appropriate, provided that it is excluded from version control through `.gitignore`.

## Installation

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required database connection settings.

## Running the Application

The Flask application can currently be run in a development environment using Flask's development server.

For example:

```bash
flask run
```

The exact startup command may change as the application architecture develops.

## Development Roadmap

The remaining work is divided into several major areas:

### Administrator Functionality

Complete the administrator interface and associated permissions for managing the library.

### Search Systems

Expand the existing search functionality to support more advanced searching and filtering.

### Due Dates and Overdue Tracking

Add due dates to borrowed books and implement logic for identifying overdue items.

### Logging

Expand the existing database logging system to provide more comprehensive application activity tracking.

### Custom Error Handling

Implement custom Flask error pages and centralized error handling for expected application errors.

### Containerization

Package the application and its dependencies into containers to make deployment more consistent.

### Production Rollout

Prepare the application for production deployment, including production server configuration, environment management, and deployment infrastructure.

## Relationship to `web_db`

`web_db` contains the terminal-based version of the Library Management System.

That project transitioned the application from using a locally managed PostgreSQL database to a remotely hosted PostgreSQL database.

`application_db` represents the next stage of development: transforming the system into a Flask web application that can be accessed through a browser.

The two repositories therefore represent different stages of the same overall project:

```text
Terminal Application
       │
       │ Remote PostgreSQL integration
       ▼
    web_db
       │
       │ Flask/web migration
       ▼
 application_db
       │
       │ Production development
       ▼
 Future Production LMS
```

## Future Goals

The ultimate goal is to turn the current Flask application into a fully deployable Library Management System with:

* Complete member functionality
* Complete administrator functionality
* Advanced searching
* Borrowing and reservation management
* Due dates and overdue tracking
* Comprehensive logging
* Robust error handling
* Secure configuration
* Containerized deployment
* Production hosting
* Automated testing

## License
```
This project is primarily intended as an educational/student project.
```

Here's an updated version of the README file, incorporating your additional instructions:

---

# CRM System

## Overview

This project is a Customer Relationship Management (CRM) system built with Python, SQLAlchemy, and PostgreSQL. The CRM system manages clients, contracts, events, and users, providing role-based access control and a robust authentication system.

## Features

- **User Management**: Create, update, delete, and authenticate users.
- **Role Management**: Define roles with specific permissions and assign them to users.
- **Client Management**: Manage clients, including creating, updating, and deleting client records.
- **Contract Management**: Manage contracts associated with clients.
- **Event Management**: Track events linked to contracts.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.11 or later
- PostgreSQL
- Virtualenv

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/crm.git
cd crm
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv crm_env
source crm_env/bin/activate  # On Windows use `crm_env\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database and user for the CRM system. Update your database connection settings in `alembic.ini` and your environment variables.

```sql
CREATE DATABASE crm_db;
CREATE USER crm_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE crm_db TO crm_user;
```

### 5. Configure Alembic

Before running any database migrations, you need to configure Alembic by setting up the correct database URL in `alembic.ini`:

```ini
# alembic.ini

[alembic]
# ...

sqlalchemy.url = postgresql://crm_user:yourpassword@localhost/crm_db
```

### 6. Initialize the Database

Run the following command to set up the database schema:

```bash
alembic upgrade head
```

### 7. Run the Application

You can explore various CLI options provided by the application using:

```bash
python cli.py --help
```

To run the application:

```bash
python3 cli.py
```

The application will be available at `http://localhost:5000`.

## Running Tests

To run the unit tests, use the following command:

```bash
python3 -m unittest discover -s tests
```

Ensure your PostgreSQL database is set up correctly before running tests.

## Deployment

To deploy the CRM system, you can follow these general steps:

1. **Set Up the Server**: Install the necessary software (Python, PostgreSQL, etc.) on your server.
2. **Clone the Repository**: Clone your project repository onto the server.
3. **Install Dependencies**: Use a virtual environment to install project dependencies.
4. **Configure Environment Variables**: Set up environment variables for production, such as database connection strings.
5. **Configure Alembic**: Ensure `alembic.ini` is set up with your production database URL.
6. **Run Database Migrations**: Initialize the database schema on the production database using Alembic.
7. **Start the Application**: Use cli.py to run the application in command line.


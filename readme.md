# CRM System

## Overview

This project is a Customer Relationship Management (CRM) system built with Python, SQLAlchemy, and SQLite. The CRM system manages clients, contracts, events, and users, providing role-based access control and a robust authentication system.

## Features

- **User Management**: Create, update, delete, and authenticate users.
- **Role Management**: Define roles with specific permissions and assign them to users.
- **Client Management**: Manage clients, including creating, updating, and deleting client records.
- **Contract Management**: Manage contracts associated with clients.
- **Event Management**: Track events linked to contracts.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.11 or later
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

### 4. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```
DATABASE_URL=sqlite:///crm.db
```

This ensures the system connects to an SQLite database file named `crm.db`.

### 5. Initialize the Database

Run the following command to set up the database schema:

```bash
alembic upgrade head
```

### 6. Run the Application

You can explore various CLI options provided by the application using:

```bash
python cli.py --help
```

To run the application:

```bash
python cli.py
```

## Running Tests

To run the unit tests, use the following command:

```bash
python -m unittest discover -s tests
```

Ensure your SQLite database is set up correctly before running tests.

## Deployment

To deploy the CRM system, you can follow these general steps:

1. **Set Up the Server**: Install the necessary software (Python, SQLite, etc.) on your server.
2. **Clone the Repository**: Clone your project repository onto the server.
3. **Install Dependencies**: Use a virtual environment to install project dependencies.
4. **Configure Environment Variables**: Set up the `.env` file with the SQLite database path.
5. **Configure Alembic**: Ensure the database migrations are properly set up.
6. **Run Database Migrations**: Initialize the database schema using Alembic.
7. **Start the Application**: Use `cli.py` to run the application via command line.


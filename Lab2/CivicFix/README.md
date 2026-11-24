# CivicFix

A database-backed REST API for reporting public maintenance issues, built using **FastAPI, SQLModel, and PostgreSQL**.

## Requirements

- Python 3.10+
- Docker Desktop
- Git

## Project Structure

```text
CivicFix/
├── main.py
├── models.py
├── database.py
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CivicFix
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install fastapi sqlmodel psycopg[binary] python-dotenv
```

### 4. Configure Environment Variables

Create a `.env` file in the project root using `.env.example` as a reference.

Update the database credentials according to your PostgreSQL configuration.

**Note:** The actual `.env` file contains private credentials and must not be submitted or committed to Git.

### 5. Start PostgreSQL

Make sure Docker Desktop is running, then execute:

```bash
docker compose up -d
```

### 6. Run the FastAPI Application

```bash
fastapi dev main.py
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation and Testing

Open Swagger UI in your browser:

**http://127.0.0.1:8000/docs**

Use Swagger UI to test the six required API operations:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users` | Create a user |
| POST | `/issues` | Create an issue |
| GET | `/issues` | Retrieve all issues |
| GET | `/issues/{issue_id}` | Retrieve an issue by ID |
| PUT | `/issues/{issue_id}` | Update an issue |
| DELETE | `/issues/{issue_id}` | Delete an issue |

The application also includes optional comment endpoints and issue filtering by status and category.

## Database Persistence

PostgreSQL stores the application data persistently using a Docker named volume. Restarting FastAPI does not delete the saved records.

To stop the database container:

```bash
docker compose stop
```

To start it again:

```bash
docker compose start
```

**Important:** Avoid `docker compose down -v` unless you intend to delete the database volume and its stored data.
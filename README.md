# Personal API

A REST API built with FastAPI and PostgreSQL for managing users. It supports creating, listing, updating and deleting users, stores passwords as bcrypt hashes instead of plain text, and includes a login endpoint that verifies a user's password.

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI, served with Uvicorn
- **Database:** PostgreSQL, accessed through SQLAlchemy and the psycopg2 driver
- **Validation:** Pydantic
- **Password hashing:** Passlib with bcrypt
- **Configuration:** python-dotenv, which loads the database connection string from a `.env` file

## Features

- Create a user (`POST /users`) with the password hashed before it is stored
- List all users (`GET /users`)
- Update a user's name and age (`PUT /users/{user_id}`)
- Delete a user (`DELETE /users/{user_id}`)
- Log in with email and password (`POST /login`), checked against the stored hash
- Database credentials kept out of the code in a `.env` file
- JWT authentication: protected update and delete routes, and users can only modify their own account
- Dockerized with Docker Compose: the API and PostgreSQL start with one command
# Setup

1. Clone the repository:
```
   git clone https://github.com/theoluwanifemi18/REST-API.git
   cd REST-API
```
2. Create and activate a virtual environment:
```
   python -m venv venv
   source venv/bin/activate
```
3. Install the dependencies:
```
   pip install -r requirements.txt
```
4. Create a PostgreSQL database and a user for it, then create a `.env` file in the project root:
```
   DATABASE_URL=postgresql://user:password@localhost/dbname
```
5. Start the server:
```
   uvicorn main:app --reload
```

## API Docs

With the server running, open http://127.0.0.1:8000/docs to see the interactive documentation and try every endpoint from the browser.
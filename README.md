# Python Todo App

A modern, secure REST API for managing todos built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- 🔐 **JWT Authentication** - Secure user authentication with access tokens
- 👥 **User Management** - User registration and role-based access control
- 📝 **Todo CRUD Operations** - Create, read, update, and delete todos
- 🔒 **Data Isolation** - Users can only access their own todos
- 👨‍💼 **Admin Panel** - Administrative functions for managing all todos
- 🧪 **Comprehensive Testing** - Unit tests with pytest
- 🗄️ **Database Migrations** - Alembic for database schema management
- 📊 **Health Check** - API health monitoring endpoint

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt with passlib
- **Testing**: pytest
- **Database Migrations**: Alembic
- **API Documentation**: Auto-generated with FastAPI

## Project Structure

```
todos/
├── alembic/                 # Database migrations
├── db/
│   ├── database.py         # Database configuration
│   └── models.py           # SQLAlchemy models
├── routers/
│   ├── auth.py             # Authentication endpoints
│   ├── todos.py            # Todo CRUD endpoints
│   └── admin.py            # Admin endpoints
├── test/                   # Test files
├── main.py                 # FastAPI application entry point
└── alembic.ini            # Alembic configuration
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd todos
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install fastapi uvicorn sqlalchemy passlib python-jose[cryptography] alembic pytest
   ```

4. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

5. **Start the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/auth`)

#### Create User

```http
POST /auth/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword",
  "role": "user"
}
```

#### Login

```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=securepassword
```

### Todos (`/todos`)

All todo endpoints require authentication. Include the JWT token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

#### Get All Todos

```http
GET /todos/
```

#### Get Single Todo

```http
GET /todos/todo/{todo_id}
```

#### Create Todo

```http
POST /todos/
Content-Type: application/json

{
  "title": "Complete project",
  "description": "Finish the todo app implementation",
  "priority": 3,
  "complete": false
}
```

#### Update Todo

```http
PUT /todos/{todo_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "priority": 4,
  "complete": true
}
```

#### Delete Todo

```http
DELETE /todos/{todo_id}
```

### Admin (`/admin`)

Admin endpoints require admin role.

#### Get All Todos (Admin)

```http
GET /admin/todo
```

#### Delete Todo (Admin)

```http
DELETE /admin/todo/{todo_id}
```

### Health Check

```http
GET /health
```

## Data Models

### User

- `id`: Primary key
- `email`: Unique email address
- `username`: Unique username
- `first_name`: User's first name
- `last_name`: User's last name
- `hashed_password`: Bcrypt hashed password
- `is_active`: Account status
- `role`: User role (user/admin)
- `phone_number`: Optional phone number

### Todo

- `id`: Primary key
- `title`: Todo title (min 3 characters)
- `description`: Todo description (3-100 characters)
- `priority`: Priority level (1-5)
- `complete`: Completion status
- `owner_id`: Foreign key to user

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=.
```

## Security Features

- **Password Hashing**: All passwords are hashed using bcrypt
- **JWT Tokens**: Secure authentication with expiring tokens
- **Role-Based Access**: Different permissions for users and admins
- **Data Isolation**: Users can only access their own todos
- **Input Validation**: Pydantic models ensure data integrity

## Environment Variables

For production, consider setting these environment variables:

- `SECRET_KEY`: JWT secret key (currently hardcoded)
- `DATABASE_URL`: Database connection string (currently local db)
- `ALGORITHM`: JWT algorithm (default: HS256)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

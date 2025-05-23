# README.md

# E-Learning Backend

This project is a backend application for an e-learning platform built using FastAPI. It provides RESTful API endpoints for managing users, courses, chapters, parts, categories, and registrations.

## Project Structure

```
Backend/
├── app/                                # Main directory containing all backend source code
│   ├── __init__.py                     # Initializes the app package
│   ├── main.py                          # Entry point of the FastAPI application
│   ├── database.py                      # Database connection configuration using SQLAlchemy
│   ├── models/                          # ORM models mapping to database tables
│   │   ├── __init__.py                  # Initializes the models package
│   │   ├── user.py                       # User model
│   │   ├── course.py                     # Course model
│   │   ├── chapter.py                    # Chapter model
│   │   ├── part.py                       # Part model
│   │   ├── category.py                   # Category model
│   │   └── registered_course.py          # RegisteredCourse model
│   ├── schemas/                         # Pydantic schemas for data validation
│   │   ├── __init__.py                   # Initializes the schemas package
│   │   ├── user.py                       # User schema
│   │   ├── course.py                     # Course schema
│   │   ├── chapter.py                    # Chapter schema
│   │   ├── part.py                       # Part schema
│   │   ├── category.py                   # Category schema
│   │   └── registered_course.py          # RegisteredCourse schema
│   ├── crud/                            # Business logic for CRUD operations
│   │   ├── __init__.py                   # Initializes the crud package
│   │   ├── user.py                       # User CRUD operations
│   │   ├── course.py                     # Course CRUD operations
│   │   ├── chapter.py                    # Chapter CRUD operations
│   │   ├── part.py                       # Part CRUD operations
│   │   ├── category.py                   # Category CRUD operations
│   │   └── registered_course.py          # RegisteredCourse CRUD operations
│   ├── routers/                         # API endpoint definitions
│   │   ├── __init__.py                   # Initializes the routers package
│   │   ├── user.py                       # User-related API endpoints
│   │   ├── course.py                     # Course-related API endpoints
│   │   ├── chapter.py                    # Chapter-related API endpoints
│   │   ├── part.py                       # Part-related API endpoints
│   │   ├── category.py                   # Category-related API endpoints
│   │   └── registered_course.py          # Registered course-related API endpoints
│   ├── auth/                            # Authentication module
│   │   ├── __init__.py                   # Initializes the auth package
│   │   ├── auth_handler.py               # JWT token creation and verification
│   │   └── auth_bearer.py                # Middleware for JWT authentication
│   └── utils/                           # Utility functions
│       ├── __init__.py                   # Initializes the utils package
│       └── helpers.py                    # Common utility functions
├── tests/                               # Unit tests for the application
│   ├── __init__.py                       # Initializes the tests package
│   ├── test_users.py                     # Unit tests for user functionalities
│   └── ...                               # Other test files
├── .env                                 # Environment variables for database connection and secrets
├── requirements.txt                     # List of required Python packages
└── README.md                            # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd Backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables in the `.env` file.

## Running the Application

To run the FastAPI application, execute the following command:
```
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Documentation

The automatically generated API documentation can be accessed at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
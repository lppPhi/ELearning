# settings.py

# ...existing code...

INSTALLED_APPS = [
    # ...existing code...
    'corsheaders',
    # ...existing code...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...existing code...
]

CORS_ALLOW_ALL_ORIGINS = True  # hoặc cấu hình domain cụ thể

# ...existing code...
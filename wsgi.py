"""
WSGI entry point for Gunicorn deployment
"""
from main import app

if __name__ == "__main__":
    app.run()
"""
WSGI entry point for Gunicorn deployment
"""
import sys
import os

# Change to backend directory
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

from app import app

if __name__ == "__main__":
    app.run()
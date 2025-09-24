"""
Vercel serverless entry point for Quantum Banking Backend
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app

# Create the Flask application
app = create_app()

# Vercel serverless function handler
def handler(request, response):
    return app(request, response)

# For local development
if __name__ == "__main__":
    app.run(debug=True)
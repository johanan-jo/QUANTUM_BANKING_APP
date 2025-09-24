#!/bin/bash
# Render.com start script

echo "🚀 Starting Quantum Banking Backend..."

# Start the Flask application with Gunicorn using wsgi.py
gunicorn --bind 0.0.0.0:$PORT wsgi:app
"""
Production WSGI entry point for Quantum Banking Backend
"""
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')

# Add both directories to sys.path
sys.path.insert(0, current_dir)
sys.path.insert(0, backend_dir)

# Set working directory to backend for relative imports
os.chdir(backend_dir)

# Now import the app
try:
    from app import app
    print("✅ Successfully imported Flask app")
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
    # Create a fallback app
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/health')
    def health():
        return {'status': 'error', 'message': 'Import failed'}

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
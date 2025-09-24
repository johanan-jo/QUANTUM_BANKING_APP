"""
Production server entry point for Quantum Banking
"""
import os
import sys

# Set up environment
os.environ.setdefault('FLASK_ENV', 'production')

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')
sys.path.insert(0, backend_dir)

# Change to backend directory for relative imports to work
original_cwd = os.getcwd()
os.chdir(backend_dir)

try:
    # Import the Flask app
    from app import app as application
    
    # Change back to original directory
    os.chdir(original_cwd)
    
    print("✅ Production server initialized successfully")
    
    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 10000))
        application.run(host='0.0.0.0', port=port)

except Exception as e:
    print(f"❌ Failed to initialize server: {e}")
    # Change back to original directory even on error
    os.chdir(original_cwd)
    raise

# Export for gunicorn
app = application
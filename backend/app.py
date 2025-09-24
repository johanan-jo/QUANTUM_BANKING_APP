"""
Quantum Banking Backend Application

A secure banking application with quantum-inspired OTP generation,
JWT authentication, and comprehensive user management.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'fallback-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS for frontend communication (allow multiple ports)
    CORS(app, origins=[
        'http://localhost:3000', 
        'http://127.0.0.1:3000',
        'http://localhost:3001', 
        'http://127.0.0.1:3001',
        'http://localhost:3002', 
        'http://127.0.0.1:3002',
        'http://localhost:3003', 
        'http://127.0.0.1:3003',
        'https://lil-3-l6z3mpuji-johanan-js-projects.vercel.app',
        'https://quantum-banking-api.onrender.com'
    ])
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Health check endpoints
    @app.route('/')
    def health_check():
        """API health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'Quantum Banking API',
            'version': '1.0.0',
            'message': 'Welcome to Quantum Banking - Secure • Reliable • Advanced'
        })
    
    @app.route('/api/health')
    def api_health():
        """Railway health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': '2025-09-11T00:00:00Z',
            'services': {
                'database': 'connected',
                'email': 'configured',
                'quantum_otp': 'active',
                'authentication': 'ready'
            },
            'endpoints': {
                'auth': {
                    'register': '/api/auth/register',
                    'login': '/api/auth/login',
                    'verify_otp': '/api/auth/verify-otp',
                    'resend_otp': '/api/auth/resend-otp'
                },
                'dashboard': {
                    'user_info': '/api/dashboard/me',
                    'transactions': '/api/dashboard/transactions',
                    'summary': '/api/dashboard/account-summary'
                }
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors"""
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.before_request
    def log_request():
        """Log incoming requests for debugging"""
        if os.getenv('DEBUG_OTP', 'false').lower() == 'true':
            print(f"[API] {request.method} {request.path}")
    
    return app

def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        'DB_HOST', 'DB_USER', 'DB_PASS', 'DB_NAME',
        'SMTP_EMAIL', 'SMTP_PASSWORD', 'JWT_SECRET'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please check your .env file and ensure all variables are set.")
        print("   Refer to .env.example for the required format.")
        return False
    
    print("✅ All required environment variables are configured")
    return True

# Create Flask app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    print("🏦 Starting Quantum Banking Backend...")
    print("=" * 50)
    
    # Validate environment
    if not validate_environment():
        print("❌ Environment validation failed. Exiting.")
        exit(1)
    
    # Get configuration
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('PORT', os.getenv('FLASK_PORT', 5000)))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Server starting on http://{host}:{port}")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print(f"🔐 JWT Secret: {'Configured' if os.getenv('JWT_SECRET') else 'Missing'}")
    print(f"📧 SMTP: {'Configured' if os.getenv('SMTP_EMAIL') else 'Missing'}")
    print(f"🗄️  Database: {os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_NAME', 'quantum_banking')}")
    print("=" * 50)
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

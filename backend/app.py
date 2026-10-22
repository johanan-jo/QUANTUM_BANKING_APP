"""
Quantum Banking Backend Application

A secure banking application with quantum-inspired OTP generation,
JWT authentication, and comprehensive user management.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("quantum_banking.app")

# Import blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET', 'fallback-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS for frontend communication
    CORS(app, 
         resources={r"/api/*": {"origins": "*"}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Health check endpoint
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
        """Detailed API health check with dynamic service inspection"""
        client_id = os.getenv('GMAIL_CLIENT_ID') or os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GMAIL_CLIENT_SECRET') or os.getenv('GOOGLE_CLIENT_SECRET')
        refresh_token = os.getenv('GMAIL_REFRESH_TOKEN') or os.getenv('GOOGLE_REFRESH_TOKEN')
        sender_email = (
            os.getenv('GMAIL_SENDER_EMAIL')
            or os.getenv('FROM_EMAIL')
            or os.getenv('SMTP_EMAIL')
        )

        missing_email_vars = []
        if not client_id:
            missing_email_vars.append('GMAIL_CLIENT_ID')
        if not client_secret:
            missing_email_vars.append('GMAIL_CLIENT_SECRET')
        if not refresh_token:
            missing_email_vars.append('GMAIL_REFRESH_TOKEN')
        if not sender_email:
            missing_email_vars.append('GMAIL_SENDER_EMAIL')

        email_status = "configured" if not missing_email_vars else "missing_credentials"

        return jsonify({
            'status': 'healthy' if not missing_email_vars else 'degraded',
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'services': {
                'database': 'connected',
                'email': {
                    'provider': 'Gmail API (OAuth 2.0)',
                    'status': email_status,
                    'missing_variables': missing_email_vars,
                    'sender_configured': bool(sender_email)
                },
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
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

# Application instance for WSGI servers
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    print("=" * 60)
    print("🏦 Quantum Banking Backend Server")
    print("=" * 60)
    print(f"Server starting on port: {port}")
    print(f"Debug mode: {debug}")
    print(f"API endpoints available at: http://localhost:{port}/api")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)

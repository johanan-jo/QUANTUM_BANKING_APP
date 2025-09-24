"""
Security utilities for password hashing and JWT token management
"""
import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hash_password):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

def generate_jwt_token(user_data):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_data['id'],
        'account_number': user_data['account_number'],
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow()
    }
    
    secret_key = os.getenv('JWT_SECRET')
    if not secret_key:
        raise ValueError("JWT_SECRET not found in environment variables")
    
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_jwt_token(token):
    """Decode and verify JWT token"""
    try:
        secret_key = os.getenv('JWT_SECRET')
        if not secret_key:
            raise ValueError("JWT_SECRET not found in environment variables")
        
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Decode token
        payload = decode_jwt_token(token)
        if payload is None:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Add user info to request context
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_account_number(account_number):
    """Validate account number format (10 digits)"""
    return account_number.isdigit() and len(account_number) == 10

def validate_password(password):
    """Validate password strength (minimum 8 characters)"""
    return len(password) >= 8

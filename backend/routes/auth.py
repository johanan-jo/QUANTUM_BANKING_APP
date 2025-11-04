"""
Authentication routes for registration, login, and OTP verification
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import os

from utils.db import (
    get_user_by_account, get_user_by_email, create_user, 
    store_otp, get_valid_otp, mark_otp_used, count_recent_otps
)
from utils.security import (
    hash_password, verify_password, generate_jwt_token,
    validate_email, validate_account_number, validate_password
)
from utils.mailer import send_otp_email, send_welcome_email
from utils.quantum_otp import generate_otp

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request Body:
        {
            "name": "John Doe",
            "account_number": "1234567890", 
            "email": "john@example.com",
            "password": "securepassword"
        }
    
    Returns:
        JSON response with success/error status
    """
    try:
        data = request.get_json()
        
        # Validate required fields (removed account_number requirement)
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate input formats
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        if len(name) < 2:
            return jsonify({'error': 'Name must be at least 2 characters long'}), 400
        
        # Check if email already exists
        existing_email = get_user_by_email(email)
        if existing_email:
            return jsonify({'error': 'Email already registered'}), 400
        
        # Auto-generate unique account number
        import random
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            if not get_user_by_account(account_number):
                break
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        create_user(name, account_number, email, password_hash)
        
        # Send welcome email (optional, doesn't affect registration success)
        try:
            send_welcome_email(email, name, account_number)
        except Exception as e:
            print(f"Failed to send welcome email: {e}")
        
        return jsonify({
            'message': 'Account created successfully',
            'account_number': account_number
        }), 201
        
    except Exception as e:
        import traceback
        print(f"Registration error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and send OTP
    
    Request Body:
        {
            "account_number": "1234567890",
            "password": "securepassword"
        }
    
    Returns:
        JSON response indicating OTP sent status
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('account_number') or not data.get('password'):
            return jsonify({'error': 'Account number and password are required'}), 400
        
        account_number = data['account_number'].strip()
        password = data['password']
        
        # Get user by account number
        user = get_user_by_account(account_number)
        if not user:
            return jsonify({'error': 'Invalid account number or password'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid account number or password'}), 401
        
        # Rate limiting: Check recent OTP requests
        recent_otps = count_recent_otps(user['id'], hours=1)
        if recent_otps >= 3:
            return jsonify({'error': 'Too many OTP requests. Please try again later.'}), 429
        
        # Generate quantum-inspired OTP
        otp_code = generate_otp(user['id'])
        
        # Set OTP expiry (5 minutes from now for better UX)
        expiry = datetime.now() + timedelta(minutes=5)
        
        # Store OTP in database
        store_otp(user['id'], otp_code, expiry)
        
        # Prepare response FIRST (don't wait for email)
        response_data = {
            'status': 'otp_sent',
            'message': 'OTP has been sent to your registered email address',
            'expiry_minutes': 5
        }
        
        # Debug mode: include OTP in response (ONLY FOR DEVELOPMENT)
        if os.getenv('DEBUG_OTP', 'false').lower() == 'true':
            response_data['debug_otp'] = otp_code
            response_data['debug_notice'] = 'OTP included for debugging - remove in production'
        
        # Send OTP via email in background (after response is sent)
        import threading
        threading.Thread(target=lambda: send_otp_email(user['email'], otp_code)).start()
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """
    Verify OTP and complete login
    
    Request Body:
        {
            "account_number": "1234567890",
            "otp": "123456"
        }
    
    Returns:
        JSON response with JWT token and user info
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('account_number') or not data.get('otp'):
            return jsonify({'error': 'Account number and OTP are required'}), 400
        
        account_number = data['account_number'].strip()
        otp_code = data['otp'].strip()
        
        # Validate OTP format
        if not otp_code.isdigit() or len(otp_code) != 6:
            return jsonify({'error': 'OTP must be 6 digits'}), 400
        
        # Get user by account number
        user = get_user_by_account(account_number)
        if not user:
            return jsonify({'error': 'Invalid account number'}), 401
        
        # Get valid OTP for user
        otp_record = get_valid_otp(user['id'], otp_code)
        if not otp_record:
            return jsonify({'error': 'Invalid or expired OTP'}), 401
        
        # Mark OTP as used
        mark_otp_used(otp_record['id'])
        
        # Generate JWT token
        token = generate_jwt_token(user)
        
        # Return user info and token
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'name': user['name'],
                'account_number': user['account_number'],
                'email': user['email']
            }
        }), 200
        
    except Exception as e:
        print(f"OTP verification error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """
    Resend OTP to user's email
    
    Request Body:
        {
            "account_number": "1234567890"
        }
    
    Returns:
        JSON response indicating OTP sent status
    """
    try:
        data = request.get_json()
        
        if not data.get('account_number'):
            return jsonify({'error': 'Account number is required'}), 400
        
        account_number = data['account_number'].strip()
        
        # Get user by account number
        user = get_user_by_account(account_number)
        if not user:
            return jsonify({'error': 'Invalid account number'}), 401
        
        # Rate limiting: Check recent OTP requests
        recent_otps = count_recent_otps(user['id'], hours=1)
        if recent_otps >= 3:
            return jsonify({'error': 'Too many OTP requests. Please try again later.'}), 429
        
        # Generate new OTP
        otp_code = generate_otp(user['id'])
        
        # Set OTP expiry (2 minutes from now)
        expiry = datetime.now() + timedelta(minutes=2)
        
        # Store OTP in database
        store_otp(user['id'], otp_code, expiry)
        
        # Send OTP via email
        email_sent = send_otp_email(user['email'], otp_code)
        if not email_sent:
            return jsonify({'error': 'Failed to send OTP email. Please try again.'}), 500
        
        # Prepare response
        response_data = {
            'status': 'otp_sent',
            'message': 'New OTP has been sent to your registered email address'
        }
        
        # Debug mode: include OTP in response (ONLY FOR DEVELOPMENT)
        if os.getenv('DEBUG_OTP', 'false').lower() == 'true':
            response_data['debug_otp'] = otp_code
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Resend OTP error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

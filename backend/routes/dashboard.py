"""
Dashboard routes for authenticated users
"""
from flask import Blueprint, request, jsonify
import random
from datetime import datetime, timedelta

from utils.security import token_required
from utils.db import get_user_by_account

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/me', methods=['GET'])
@token_required
def get_user_dashboard():
    """
    Get user dashboard information (protected route)
    
    Headers:
        Authorization: Bearer <jwt_token>
    
    Returns:
        JSON response with user dashboard data
    """
    try:
        # Get current user from token
        current_user = request.current_user
        
        # Get fresh user data from database
        user = get_user_by_account(current_user['account_number'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate dummy balance (in production, this would come from accounts table)
        random.seed(user['id'])  # Consistent random for same user
        balance = round(random.uniform(1000, 50000), 2)
        
        # Generate dummy recent transactions
        transactions = []
        for i in range(5):
            transaction_date = datetime.now() - timedelta(days=random.randint(1, 30))
            amount = round(random.uniform(-500, 1000), 2)
            transaction_type = "Credit" if amount > 0 else "Debit"
            
            # Generate random transaction descriptions
            descriptions = [
                "ATM Withdrawal", "Online Transfer", "Salary Credit", "Bill Payment",
                "Shopping", "Restaurant", "Fuel Payment", "Interest Credit",
                "Dividend Credit", "Insurance Payment", "Loan EMI", "Mobile Recharge"
            ]
            
            transactions.append({
                'id': f"TXN{user['id']}{i:03d}",
                'date': transaction_date.strftime('%Y-%m-%d'),
                'description': random.choice(descriptions),
                'amount': abs(amount),
                'type': transaction_type,
                'balance_after': balance + random.uniform(-100, 100)
            })
        
        # Sort transactions by date (newest first)
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        # Calculate some dummy statistics
        total_credits = sum(t['amount'] for t in transactions if t['type'] == 'Credit')
        total_debits = sum(t['amount'] for t in transactions if t['type'] == 'Debit')
        
        dashboard_data = {
            'user': {
                'id': user['id'],
                'name': user['name'],
                'account_number': user['account_number'],
                'email': user['email'],
                'member_since': user['created_at'].strftime('%B %Y') if user.get('created_at') else 'Recently'
            },
            'account': {
                'balance': balance,
                'currency': 'USD',
                'account_type': 'Quantum Savings',
                'status': 'Active'
            },
            'recent_transactions': transactions,
            'monthly_summary': {
                'total_credits': round(total_credits, 2),
                'total_debits': round(total_debits, 2),
                'net_change': round(total_credits - total_debits, 2),
                'transaction_count': len(transactions)
            },
            'quick_actions': [
                {
                    'id': 'transfer',
                    'title': 'Transfer Money',
                    'description': 'Send money to another account',
                    'icon': '💸'
                },
                {
                    'id': 'pay_bills',
                    'title': 'Pay Bills',
                    'description': 'Pay utilities and services',
                    'icon': '💡'
                },
                {
                    'id': 'statements',
                    'title': 'Statements',
                    'description': 'Download account statements',
                    'icon': '📄'
                },
                {
                    'id': 'support',
                    'title': 'Support',
                    'description': 'Contact customer support',
                    'icon': '🎧'
                }
            ]
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        print(f"Dashboard error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@dashboard_bp.route('/transactions', methods=['GET'])
@token_required
def get_transactions():
    """
    Get user transaction history with pagination
    
    Query Parameters:
        page (int): Page number (default: 1)
        limit (int): Items per page (default: 10, max: 50)
        type (str): Filter by transaction type ('credit' or 'debit')
    
    Returns:
        JSON response with paginated transactions
    """
    try:
        current_user = request.current_user
        
        # Get query parameters
        page = int(request.args.get('page', 1))
        limit = min(int(request.args.get('limit', 10)), 50)  # Max 50 items per page
        transaction_type = request.args.get('type', '').lower()
        
        # Get user data
        user = get_user_by_account(current_user['account_number'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate dummy transactions (in production, query from database)
        random.seed(user['id'])
        all_transactions = []
        
        for i in range(50):  # Generate 50 dummy transactions
            transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
            amount = round(random.uniform(-1000, 2000), 2)
            txn_type = "credit" if amount > 0 else "debit"
            
            descriptions = [
                "ATM Withdrawal", "Online Transfer", "Salary Credit", "Bill Payment",
                "Shopping", "Restaurant", "Fuel Payment", "Interest Credit",
                "Dividend Credit", "Insurance Payment", "Loan EMI", "Mobile Recharge",
                "Investment", "Refund", "Cash Deposit", "Check Deposit"
            ]
            
            all_transactions.append({
                'id': f"TXN{user['id']}{i:03d}",
                'date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
                'description': random.choice(descriptions),
                'amount': abs(amount),
                'type': txn_type,
                'reference': f"REF{random.randint(100000, 999999)}",
                'status': 'completed'
            })
        
        # Sort by date (newest first)
        all_transactions.sort(key=lambda x: x['date'], reverse=True)
        
        # Filter by type if specified
        if transaction_type in ['credit', 'debit']:
            all_transactions = [t for t in all_transactions if t['type'] == transaction_type]
        
        # Implement pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit
        transactions = all_transactions[start_index:end_index]
        
        total_transactions = len(all_transactions)
        total_pages = (total_transactions + limit - 1) // limit
        
        return jsonify({
            'transactions': transactions,
            'pagination': {
                'current_page': page,
                'total_pages': total_pages,
                'total_transactions': total_transactions,
                'per_page': limit,
                'has_next': page < total_pages,
                'has_prev': page > 1
            }
        }), 200
        
    except ValueError:
        return jsonify({'error': 'Invalid pagination parameters'}), 400
    except Exception as e:
        print(f"Transactions error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@dashboard_bp.route('/account-summary', methods=['GET'])
@token_required
def get_account_summary():
    """
    Get account summary with statistics
    
    Returns:
        JSON response with account summary data
    """
    try:
        current_user = request.current_user
        
        user = get_user_by_account(current_user['account_number'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate consistent dummy data
        random.seed(user['id'])
        
        # Account summary data
        summary = {
            'account_info': {
                'account_number': user['account_number'],
                'account_type': 'Quantum Savings',
                'branch': 'Digital Branch',
                'ifsc_code': 'QNTM0001234',
                'opened_date': user['created_at'].strftime('%Y-%m-%d') if user.get('created_at') else '2024-01-01'
            },
            'balances': {
                'current_balance': round(random.uniform(5000, 75000), 2),
                'available_balance': round(random.uniform(4000, 70000), 2),
                'minimum_balance': 1000.00,
                'overdraft_limit': 0.00
            },
            'monthly_stats': {
                'credits_count': random.randint(5, 20),
                'debits_count': random.randint(10, 30),
                'total_credits': round(random.uniform(3000, 15000), 2),
                'total_debits': round(random.uniform(2000, 12000), 2),
                'average_transaction': round(random.uniform(200, 800), 2)
            },
            'yearly_stats': {
                'total_credits': round(random.uniform(30000, 150000), 2),
                'total_debits': round(random.uniform(25000, 120000), 2),
                'interest_earned': round(random.uniform(500, 2000), 2),
                'service_charges': round(random.uniform(50, 200), 2)
            },
            'preferences': {
                'statement_frequency': 'Monthly',
                'notification_method': 'Email & SMS',
                'auto_sweep': False,
                'mobile_banking': True
            }
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        print(f"Account summary error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

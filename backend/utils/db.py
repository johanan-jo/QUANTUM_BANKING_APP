"""
Database connection utilities with connection pooling (Supabase/PostgreSQL)
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
import os
from contextlib import contextmanager

class DatabasePool:
    """Simple database connection manager for PostgreSQL/Supabase"""
    
    def __init__(self):
        # Support both DATABASE_URL (standard Postgres) and individual params
        self.database_url = os.getenv('DATABASE_URL')
        
        if self.database_url:
            # Use DATABASE_URL if provided (Supabase, Railway, etc.)
            self.connection_string = self.database_url
        else:
            # Fallback to individual parameters
            host = os.getenv('DB_HOST', 'localhost')
            user = os.getenv('DB_USER', 'postgres')
            password = os.getenv('DB_PASS', '')
            database = os.getenv('DB_NAME', 'quantum_banking')
            port = os.getenv('DB_PORT', '5432')
            
            self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        
        # Initialize connection pool for better performance
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1,  # min connections
                10,  # max connections
                self.connection_string
            )
        except Exception as e:
            print(f"Warning: Could not create connection pool: {e}")
            self.connection_pool = None
    
    def get_connection(self):
        """Get a connection from the pool or create a new one"""
        if self.connection_pool:
            try:
                return self.connection_pool.getconn()
            except Exception:
                pass
        
        # Fallback to direct connection
        return psycopg2.connect(self.connection_string)
    
    def return_connection(self, connection):
        """Return connection to the pool"""
        if self.connection_pool and connection:
            try:
                self.connection_pool.putconn(connection)
                return
            except Exception:
                pass
        
        # Fallback: close the connection
        if connection:
            connection.close()
    
    @contextmanager
    def get_cursor(self):
        """Context manager for database operations"""
        connection = None
        try:
            connection = self.get_connection()
            connection.autocommit = True
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                yield cursor
        except Exception as e:
            if connection:
                try:
                    connection.rollback()
                except Exception:
                    pass
            raise e
        finally:
            if connection:
                self.return_connection(connection)

# Global database pool instance
db_pool = DatabasePool()

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a database query with parameters
    
    Args:
        query (str): SQL query
        params (tuple): Query parameters
        fetch_one (bool): Whether to fetch one result
        fetch_all (bool): Whether to fetch all results
    
    Returns:
        Result based on fetch parameters
    """
    with db_pool.get_cursor() as cursor:
        cursor.execute(query, params)
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch_all:
            return cursor.fetchall()
        else:
            return cursor.rowcount

def get_user_by_account(account_number):
    """Get user by account number"""
    query = "SELECT * FROM users WHERE account_number = %s"
    return execute_query(query, (account_number,), fetch_one=True)

def get_user_by_email(email):
    """Get user by email"""
    query = "SELECT * FROM users WHERE email = %s"
    return execute_query(query, (email,), fetch_one=True)

def create_user(name, account_number, email, password_hash):
    """Create a new user"""
    query = """
    INSERT INTO users (name, account_number, email, password_hash) 
    VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (name, account_number, email, password_hash))

def store_otp(user_id, otp_code, expiry):
    """Store OTP for user"""
    query = """
    INSERT INTO otps (user_id, otp_code, expiry) 
    VALUES (%s, %s, %s)
    """
    return execute_query(query, (user_id, otp_code, expiry))

def get_valid_otp(user_id, otp_code):
    """Get valid OTP for user"""
    query = """
    SELECT * FROM otps 
    WHERE user_id = %s AND otp_code = %s AND used = FALSE AND expiry > NOW()
    ORDER BY created_at DESC LIMIT 1
    """
    return execute_query(query, (user_id, otp_code), fetch_one=True)

def mark_otp_used(otp_id):
    """Mark OTP as used"""
    query = "UPDATE otps SET used = TRUE WHERE id = %s"
    return execute_query(query, (otp_id,))

def count_recent_otps(user_id, hours=1):
    """Count recent OTPs for rate limiting"""
    query = """
    SELECT COUNT(*) as count FROM otps 
    WHERE user_id = %s AND created_at > NOW() - INTERVAL '%s hours'
    """
    result = execute_query(query, (user_id, hours), fetch_one=True)
    return result['count'] if result else 0

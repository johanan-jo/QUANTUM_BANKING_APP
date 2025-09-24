"""
Test database connection and environment variables
"""
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("🔍 Environment Variables:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASS: {os.getenv('DB_PASS')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print()

# Test database connection
try:
    from utils.db import DatabasePool
    print("🔗 Testing database connection...")
    pool = DatabasePool()
    conn = pool.get_connection()
    print("✅ Database connection successful!")
    
    # Test a simple query
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as user_count FROM users")
    result = cursor.fetchone()
    print(f"📊 Users in database: {result['user_count']}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")

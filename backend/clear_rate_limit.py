"""
Clear OTP rate limiting records from database
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from utils.db import execute_query
from datetime import datetime

def clear_rate_limits():
    """Clear all OTP records to reset rate limiting"""
    try:
        # Get count before deletion
        result = execute_query("SELECT COUNT(*) as count FROM otps", fetch_one=True)
        count_before = result['count'] if result else 0
        
        # Delete all OTP records
        execute_query("DELETE FROM otps")
        
        # Get count after deletion
        result = execute_query("SELECT COUNT(*) as count FROM otps", fetch_one=True)
        count_after = result['count'] if result else 0
        
        print("=" * 60)
        print("🔓 Rate Limit Cleared!")
        print("=" * 60)
        print(f"✅ Deleted {count_before - count_after} OTP records")
        print(f"✅ Current OTP records: {count_after}")
        print("\n🎉 You can now login and request OTP again!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clear_rate_limits()

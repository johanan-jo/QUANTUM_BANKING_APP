"""
Script to create sample users with properly hashed passwords
Run this to add test users to your database
"""

import bcrypt
import pymysql
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_sample_user():
    """Create a sample user in the database"""
    try:
        # Database configuration
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASS', ''),
            'database': os.getenv('DB_NAME', 'quantum_banking'),
            'charset': 'utf8mb4'
        }
        
        # Connect to database
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            # Sample user data
            sample_users = [
                {
                    'name': 'Alice Johnson',
                    'account_number': '2222333344',
                    'email': 'alice.johnson@example.com',
                    'password': 'password123'
                },
                {
                    'name': 'Charlie Brown',
                    'account_number': '4444555566',
                    'email': 'charlie.brown@example.com',
                    'password': 'securepass456'
                },
                {
                    'name': 'Diana Prince',
                    'account_number': '7777888899',
                    'email': 'diana.prince@example.com',
                    'password': 'strongpass789'
                }
            ]
            
            print("Creating sample users...")
            print("-" * 50)
            
            for user_data in sample_users:
                # Hash the password
                hashed_password = hash_password(user_data['password'])
                
                # Check if user already exists
                cursor.execute(
                    "SELECT id FROM users WHERE account_number = %s OR email = %s",
                    (user_data['account_number'], user_data['email'])
                )
                
                existing_user = cursor.fetchone()
                if existing_user:
                    print(f"❌ User {user_data['name']} already exists (Account: {user_data['account_number']})")
                    continue
                
                # Insert new user
                cursor.execute(
                    """
                    INSERT INTO users (name, account_number, email, password_hash) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user_data['name'], user_data['account_number'], 
                     user_data['email'], hashed_password)
                )
                
                print(f"✅ Created user: {user_data['name']}")
                print(f"   Account: {user_data['account_number']}")
                print(f"   Email: {user_data['email']}")
                print(f"   Password: {user_data['password']}")
                print(f"   Hashed: {hashed_password[:50]}...")
                print()
            
            # Commit changes
            connection.commit()
            print("✅ All sample users created successfully!")
            
    except Exception as e:
        print(f"❌ Error creating sample users: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

def generate_hash_for_password():
    """Generate bcrypt hash for a custom password"""
    print("\n" + "="*50)
    print("PASSWORD HASH GENERATOR")
    print("="*50)
    
    password = input("Enter password to hash: ")
    if password:
        hashed = hash_password(password)
        print(f"\nOriginal password: {password}")
        print(f"Bcrypt hash: {hashed}")
        print("\nUse this hash in your SQL INSERT statements.")
    else:
        print("No password entered.")

def main():
    """Main function"""
    print("🏦 Quantum Banking - Sample User Creator")
    print("="*50)
    
    while True:
        print("\nChoose an option:")
        print("1. Create sample users in database")
        print("2. Generate hash for custom password")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            create_sample_user()
        elif choice == '2':
            generate_hash_for_password()
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

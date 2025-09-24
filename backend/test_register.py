"""
Test registration endpoint directly
"""
import requests
import json

# Test data (removed account_number)
test_user = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "TestPassword123!"
}

try:
    print("🧪 Testing registration endpoint...")
    print(f"📤 Sending request to: http://127.0.0.1:5000/auth/register")
    print(f"📋 Data: {test_user}")
    
    response = requests.post(
        "http://127.0.0.1:5000/auth/register",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\n📊 Response Status: {response.status_code}")
    print(f"📄 Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"✅ Success: {response.json()}")
    else:
        print(f"❌ Error Response: {response.text}")
        try:
            error_json = response.json()
            print(f"📋 Error JSON: {error_json}")
        except:
            print("📋 Could not parse error as JSON")
            
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to backend server. Make sure it's running on port 5000.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")

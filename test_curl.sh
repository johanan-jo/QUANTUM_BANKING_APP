#!/bin/bash

# Quick API Test Script using cURL
# This script provides simple curl commands to test the Quantum Banking API

BASE_URL="http://localhost:5000/api"
CONTENT_TYPE="Content-Type: application/json"

echo "🏦 Quantum Banking - Quick API Test"
echo "=================================="
echo

# Test 1: Health Check
echo "1. Testing API Health Check..."
echo "Command: curl -X GET $BASE_URL/../"
curl -X GET http://localhost:5000/ | jq '.' 2>/dev/null || echo "Response received (install jq for formatted output)"
echo -e "\n"

# Test 2: User Registration
echo "2. Testing User Registration..."
echo "Command: curl -X POST $BASE_URL/auth/register -H '$CONTENT_TYPE' -d {...}"
curl -X POST $BASE_URL/auth/register \
  -H "$CONTENT_TYPE" \
  -d '{
    "name": "Test User cURL",
    "account_number": "5555666677",
    "email": "testcurl@example.com",
    "password": "testpassword123"
  }' | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 3: User Login (with existing account)
echo "3. Testing User Login..."
echo "Command: curl -X POST $BASE_URL/auth/login -H '$CONTENT_TYPE' -d {...}"
RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "$CONTENT_TYPE" \
  -d '{
    "account_number": "1234567890",
    "password": "password123"
  }')

echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

# Extract debug OTP if available
DEBUG_OTP=$(echo "$RESPONSE" | jq -r '.debug_otp // empty' 2>/dev/null)
if [ ! -z "$DEBUG_OTP" ]; then
    echo "Debug OTP found: $DEBUG_OTP"
    
    echo -e "\n4. Testing OTP Verification..."
    echo "Command: curl -X POST $BASE_URL/auth/verify-otp -H '$CONTENT_TYPE' -d {...}"
    TOKEN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/verify-otp \
      -H "$CONTENT_TYPE" \
      -d "{
        \"account_number\": \"1234567890\",
        \"otp\": \"$DEBUG_OTP\"
      }")
    
    echo "$TOKEN_RESPONSE" | jq '.' 2>/dev/null || echo "$TOKEN_RESPONSE"
    
    # Extract token
    TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.token // empty' 2>/dev/null)
    if [ ! -z "$TOKEN" ]; then
        echo "Token received: ${TOKEN:0:50}..."
        
        echo -e "\n5. Testing Protected Dashboard Access..."
        echo "Command: curl -X GET $BASE_URL/dashboard/me -H 'Authorization: Bearer \$TOKEN'"
        curl -X GET $BASE_URL/dashboard/me \
          -H "Authorization: Bearer $TOKEN" \
          -H "$CONTENT_TYPE" | jq '.' 2>/dev/null || echo "Response received"
        echo -e "\n"
        
        echo "6. Testing Transactions Access..."
        echo "Command: curl -X GET $BASE_URL/dashboard/transactions -H 'Authorization: Bearer \$TOKEN'"
        curl -X GET $BASE_URL/dashboard/transactions \
          -H "Authorization: Bearer $TOKEN" \
          -H "$CONTENT_TYPE" | jq '.' 2>/dev/null || echo "Response received"
    else
        echo "No token received - check OTP verification"
    fi
else
    echo "No debug OTP found. Manual OTP entry required."
    echo -e "\nTo continue testing:"
    echo "1. Check your email for the OTP"
    echo "2. Run: curl -X POST $BASE_URL/auth/verify-otp -H '$CONTENT_TYPE' -d '{\"account_number\":\"1234567890\",\"otp\":\"YOUR_OTP\"}'"
fi

echo -e "\n=================================="
echo "Test completed! 🎉"
echo
echo "Available endpoints:"
echo "  POST /api/auth/register    - Register new user"
echo "  POST /api/auth/login       - Login and request OTP"
echo "  POST /api/auth/verify-otp  - Verify OTP and get token"
echo "  POST /api/auth/resend-otp  - Resend OTP"
echo "  GET  /api/dashboard/me     - Get user dashboard (protected)"
echo "  GET  /api/dashboard/transactions - Get transactions (protected)"
echo "  GET  /api/dashboard/account-summary - Get account summary (protected)"

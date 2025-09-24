#!/bin/bash

# Render.com Deployment Script
# This script helps automate some deployment steps

echo "🚀 Quantum Banking App - Render Deployment Helper"
echo "================================================"

# Check if render.yaml exists
if [ -f "render.yaml" ]; then
    echo "✅ render.yaml found"
else
    echo "❌ render.yaml not found"
    exit 1
fi

# Check if all required files exist
files=("build.sh" "start.sh" "requirements.txt" "backend/app.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file found"
    else
        echo "❌ $file not found"
        exit 1
    fi
done

echo ""
echo "📋 Deployment Checklist:"
echo "1. Go to https://render.com"
echo "2. Sign up/Login with GitHub"
echo "3. Click 'New +' → 'Web Service'"
echo "4. Select your GitHub repository: QUANTUM_BANKING_APP"
echo "5. Render will auto-detect render.yaml and deploy!"
echo ""
echo "🌐 Your app will be available at: https://quantum-banking-api.onrender.com"
echo "📧 Test with: curl https://quantum-banking-api.onrender.com/health"
echo ""
echo "✨ All files are ready for deployment!"
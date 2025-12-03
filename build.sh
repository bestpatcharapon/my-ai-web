#!/bin/bash
set -e  # Exit on error

echo "===== Starting Build Process ====="

echo "Step 1: Installing Node.js dependencies..."
npm install

echo "Step 2: Building React app..."
npm run build

echo "Step 3: Verifying build output..."
if [ -d "dist" ]; then
    echo "✓ dist/ folder created successfully"
    ls -la dist/
else
    echo "✗ ERROR: dist/ folder not found!"
    exit 1
fi

echo "Step 4: Installing Python dependencies..."
pip install -r requirements.txt

echo "===== Build Complete ====="

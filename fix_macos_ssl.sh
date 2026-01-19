#!/bin/bash
# Quick fix for macOS SSL certificate issues

echo "========================================="
echo "macOS SSL Certificate Fix"
echo "========================================="
echo ""

# Detect Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
echo "Detected Python version: $PYTHON_VERSION"

# Find the Install Certificates command
CERT_COMMAND="/Applications/Python ${PYTHON_VERSION}/Install Certificates.command"

if [ -f "$CERT_COMMAND" ]; then
    echo ""
    echo "Found certificate installer at:"
    echo "$CERT_COMMAND"
    echo ""
    echo "Running certificate installer..."
    "$CERT_COMMAND"
    echo ""
    echo "✅ SSL certificates installed!"
else
    echo ""
    echo "⚠️  Could not find Install Certificates.command"
    echo ""
    echo "Please try one of these solutions:"
    echo ""
    echo "Option 1: Install certificates manually"
    echo "  1. Open Finder"
    echo "  2. Go to /Applications/Python ${PYTHON_VERSION}/"
    echo "  3. Double-click 'Install Certificates.command'"
    echo ""
    echo "Option 2: Use Homebrew Python (recommended)"
    echo "  brew install python"
    echo ""
    echo "Option 3: Install certifi package"
    echo "  pip3 install --upgrade certifi"
fi

echo ""
echo "========================================="

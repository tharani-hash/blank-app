#!/bin/bash
# Quick Start Script for Data Analysis Pipeline App

echo "=================================="
echo "🚀 Data Analysis Pipeline App"
echo "=================================="
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "📦 Installing required packages..."
    pip install -r requirements.txt
    echo "✅ Packages installed!"
    echo ""
fi

echo "🌐 Starting Streamlit App..."
echo "📍 Open your browser to: http://localhost:8501"
echo ""
echo "⏸️  Press Ctrl+C to stop the app"
echo ""

# Run the Streamlit app
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false

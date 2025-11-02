#!/bin/bash
# Build script for Render deployment

echo "🚀 Starting EvolveEdu.AI deployment..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Navigate to backend directory
cd evolveedu-ai/backend

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate --no-input

echo "✅ Build completed successfully!"

#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Installing dependencies..."
pip install -r requirements.txt

echo "🧹 Collecting static files..."
python manage.py collectstatic --no-input

echo "📦 Running makemigrations..."
python manage.py makemigrations --no-input

echo "📂 Running migrate..."
python manage.py migrate --no-input

echo "✅ Build script completed!"
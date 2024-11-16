#!/bin/sh

# Wait for the PostgreSQL database to be ready
./wait-for-db.sh

# Remove any existing migrations if they exist
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Make migrations for all apps
python manage.py makemigrations users
python manage.py makemigrations assets

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the Django development server
exec "$@"

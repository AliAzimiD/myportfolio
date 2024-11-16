#!/bin/sh

set -e

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing"

# Create Django admin superuser
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', 
                                '$DJANGO_SUPERUSER_EMAIL', 
                                '$DJANGO_SUPERUSER_PASSWORD')
    print('Django admin superuser created')
else:
    print('Django admin superuser already exists')
END

exec "$@"

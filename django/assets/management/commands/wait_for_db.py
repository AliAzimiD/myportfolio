# django/assets/management/commands/wait_for_db.py

"""
Django management command that waits for database to be available.

This command is useful in Docker/container environments where the web application 
needs to wait for the database service to be fully ready before proceeding.

Usage:
    python manage.py wait_for_db
"""

import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Django command to pause execution until database is available.
    
    Attempts to connect to the database, retrying every second if the connection fails.
    This prevents race conditions when starting services in Docker Compose.
    """
    
    help = 'Waits for database to be available'

    def handle(self, *args, **options):
        """
        Command handler that implements the waiting logic.
        
        Continuously attempts database connection until successful.
        Prints status messages to stdout.
        """
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))
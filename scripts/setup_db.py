#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_site.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])

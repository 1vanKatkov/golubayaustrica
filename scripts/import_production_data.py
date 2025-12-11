#!/usr/bin/env python
"""
Script to import poker session data from CSV file into production database.
Usage: python scripts/import_production_data.py
"""

import os
import sys
import csv
from decimal import Decimal
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poker_site.settings')

import django
django.setup()

from home.models import Player, PokerSession, SessionResult

def parse_decimal(value):
    """Parse decimal value, handling commas and empty strings."""
    if not value or value.strip() == '':
        return None
    # Replace comma with dot for decimal parsing
    return Decimal(str(value).replace(',', '.').replace(' ', ''))

def import_data():
    """Import data from data.csv file."""
    csv_path = 'data.csv'

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found!")
        return

    print("Starting data import...")

    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Read header
        header = next(reader)
        dates = []
        for col in header[1:]:  # Skip 'player' column
            try:
                # Parse date from format DD.MM.YYYY
                date_obj = datetime.strptime(col, '%d.%m.%Y')
                dates.append(date_obj.date())
            except ValueError:
                print(f"Warning: Could not parse date '{col}', skipping column")
                dates.append(None)

        # Process each row
        for row in reader:
            player_name = row[0].strip()
            if not player_name:
                continue

            # Get or create player
            player, created = Player.objects.get_or_create(
                name=player_name,
                defaults={
                    'description': '',
                    'photo_filename': 'anon.jpg'
                }
            )

            if created:
                print(f"Created player: {player_name}")

            # Process results for each date
            for i, result_str in enumerate(row[1:], 1):
                if i > len(dates) or dates[i-1] is None:
                    continue

                result = parse_decimal(result_str)
                if result is not None:
                    # Create session if it doesn't exist
                    session, session_created = PokerSession.objects.get_or_create(
                        date=dates[i-1],
                        defaults={'notes': ''}
                    )

                    if session_created:
                        print(f"Created session for {dates[i-1]}")

                    # Create or update result
                    result_obj, result_created = SessionResult.objects.get_or_create(
                        player=player,
                        session=session,
                        defaults={'result': result}
                    )

                    if result_created:
                        print(f"Added result for {player_name} on {dates[i-1]}: {result}")
                    else:
                        # Update existing result
                        result_obj.result = result
                        result_obj.save()
                        print(f"Updated result for {player_name} on {dates[i-1]}: {result}")

    print("Data import completed!")

if __name__ == '__main__':
    import_data()

#!/usr/bin/env python
"""Utility for running administrative Django commands."""
import os
import sys


def main():
    """Prepare the environment and delegate to Django's CLI."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker_site.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and "
            "available on your PYTHONPATH environment variable."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


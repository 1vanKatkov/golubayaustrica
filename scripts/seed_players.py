"""Populate Player records from static/photo folder."""
import sys
from pathlib import Path

import django

ROOT_DIR = Path(__file__).resolve().parent.parent
PLAYER_PHOTO_DIR = ROOT_DIR / "home" / "static" / "photo"


def main() -> None:
    """Import photos as Player entries."""
    import os

    sys.path.append(str(ROOT_DIR))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker_site.settings")
    django.setup()

    from home.models import Player

    for photo in sorted(PLAYER_PHOTO_DIR.iterdir()):
        if not photo.is_file():
            continue
        if photo.name.startswith("."):
            continue
        name = photo.stem
        player, created = Player.objects.get_or_create(
            photo_filename=photo.name,
            defaults={"name": name, "description": ""},
        )
        if not created and player.name != name:
            player.name = name
            player.description = ""
            player.save()
        if created:
            print(f"created {player.name}")
    Player.objects.filter(photo_filename=".gitkeep").delete()
    print("Players synced")


if __name__ == "__main__":
    main()


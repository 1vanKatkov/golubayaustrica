from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                (
                    "photo_filename",
                    models.CharField(
                        help_text="Имя файла из папки static/photo, например `ivan.png`.",
                        max_length=100,
                    ),
                ),
                ("description", models.TextField(blank=True)),
            ],
        )
    ]


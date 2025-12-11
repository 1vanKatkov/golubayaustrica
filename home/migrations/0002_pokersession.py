from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PokerSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("date", models.DateTimeField()),
            ],
            options={
                "ordering": ["-date"],
                "verbose_name": "покерная сессия",
                "verbose_name_plural": "покерные сессии",
            },
        ),
    ]


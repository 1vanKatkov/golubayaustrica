from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_pokersession"),
    ]

    operations = [
        migrations.CreateModel(
            name="SessionResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("player", models.ForeignKey(on_delete=models.CASCADE, to="home.player")),
                ("session", models.ForeignKey(on_delete=models.CASCADE, to="home.pokersession")),
                (
                    "result",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
            ],
            options={
                "verbose_name": "результат сессии",
                "verbose_name_plural": "результаты сессий",
                "ordering": ["session", "-result"],
            },
        ),
    ]




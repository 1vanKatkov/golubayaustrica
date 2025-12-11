from django.db import models


class Player(models.Model):
    """Represents a featured poker club member."""

    name = models.CharField(max_length=120)
    photo_filename = models.CharField(
        max_length=100,
        default="anon.jpg",
        help_text="Имя файла из папки static/photo, например `ivan.png`.",
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class PokerSession(models.Model):
    """Logs a poker session instance."""

    date = models.DateTimeField()

    class Meta:
        verbose_name = "покерная сессия"
        verbose_name_plural = "покерные сессии"
        ordering = ["-date"]

    def __str__(self):
        return f"#{self.id} — {self.date.strftime('%d.%m.%Y %H:%M')}"


class SessionResult(models.Model):
    """Records a player result for a given session."""

    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="results"
    )
    session = models.ForeignKey(
        PokerSession, on_delete=models.CASCADE, related_name="results"
    )
    result = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "результат сессии"
        verbose_name_plural = "результаты сессий"
        ordering = ["session", "-result"]

    def __str__(self):
        return f"{self.player.name} — #{self.session.id}: {self.result}"


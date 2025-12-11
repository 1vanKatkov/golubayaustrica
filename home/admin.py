from django.contrib import admin

from .models import Player, PokerSession, SessionResult


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "photo_filename")


@admin.register(PokerSession)
class PokerSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "date")
    ordering = ("-date",)


@admin.register(SessionResult)
class SessionResultAdmin(admin.ModelAdmin):
    list_display = ("player", "session", "result")
    list_filter = ("session",)


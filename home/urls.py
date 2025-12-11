from django.urls import path

from .views import (
    hall_of_fame,
    landing,
    new_session,
    session_detail,
    sessions_list,
    top_players,
)

urlpatterns = [
    path("", landing, name="landing"),
    path("sessions/new/", new_session, name="new_session"),
    path("sessions/", sessions_list, name="sessions"),
    path("sessions/<int:pk>/", session_detail, name="session_detail"),
    path("top/", top_players, name="top_players"),
    path("hall/", hall_of_fame, name="hall_of_fame"),
]


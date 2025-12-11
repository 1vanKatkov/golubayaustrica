from decimal import Decimal
import json

from django.db.models import Case, Count, DecimalField, IntegerField, Q, Value, When, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.utils import timezone

from .models import PokerSession, Player, SessionResult


def _clean_desc(text: str | None) -> str:
    if not text:
        return ""
    return text.replace("\\u002D", "-")


def _player_carousel_data():
    players_queryset = (
        Player.objects.annotate(
            total=Coalesce(
                Sum("results__result"),
                Value(Decimal("0")),
                output_field=DecimalField(),
            ),
            has_custom_photo=Case(
                When(
                    photo_filename__isnull=False,
                    photo_filename__iexact="anon.jpg",
                    then=Value(0),
                ),
                default=Value(1),
                output_field=IntegerField(),
            ),
        )
        .order_by("-has_custom_photo", "id")
    )
    return [
        {
            "id": player.id,
            "name": player.name,
            "photo": player.photo_filename,
            "description": _clean_desc(player.description),
            "total": float(player.total or 0),
        }
        for player in players_queryset
    ]


def landing(request):
    """Display the poker club landing page with roster highlights."""
    base_qs = Player.objects.annotate(
        total=Coalesce(
            Sum("results__result"),
            Value(Decimal("0")),
            output_field=DecimalField(),
        ),
        has_custom_photo=Case(
            When(
                photo_filename__isnull=False,
                photo_filename__iexact="anon.jpg",
                then=Value(0),
            ),
            default=Value(1),
            output_field=IntegerField(),
        ),
    ).order_by("-has_custom_photo", "id")

    players = list(base_qs)
    for player in players:
        player.description = _clean_desc(player.description)

    slider_players = [
        p for p in players if p.description and p.description.strip() != ""
    ]

    # Найти индекс игрока "Ваня К" в slider_players для центрирования
    center_player_index = None
    for i, player in enumerate(slider_players):
        if player.name == "Ваня К":
            center_player_index = i
            break

    return render(
        request,
        "home/index.html",
        {
            "players": players,
            "slider_players": slider_players,
            "center_player_index": center_player_index,
            "players_json": json.dumps(_player_carousel_data()),
        },
    )


def top_players(request):
    top_players_queryset = (
        Player.objects.annotate(
            total=Coalesce(
                Sum("results__result"),
                Value(Decimal("0")),
                output_field=DecimalField(),
            )
        )
        .annotate(session_count=Count("results"))
        .order_by("-total")
    )
    top_players = []
    for player_data in top_players_queryset:
        results_qs = player_data.results.select_related("session").order_by("-session__date")
        best_result = player_data.results.select_related("session").order_by("-result").first()
        worst_result = player_data.results.select_related("session").order_by("result").first()
        player_data.description = _clean_desc(player_data.description)
        recent_sessions = []
        for result in results_qs[:3]:
            recent_sessions.append(
                {
                    "session_id": result.session.id,
                    "date": result.session.date.strftime("%d.%m.%Y"),
                    "result": str(result.result),
                }
            )
        script_id = f"recent-data-{player_data.id}"
        top_players.append(
            {
                "player": player_data,
                "total": player_data.total,
                "best": {
                    "id": best_result.session.id if best_result else "",
                    "date": best_result.session.date.strftime("%d.%m.%Y") if best_result else "",
                    "result": best_result.result if best_result else "",
                },
                "worst": {
                    "id": worst_result.session.id if worst_result else "",
                    "date": worst_result.session.date.strftime("%d.%m.%Y") if worst_result else "",
                    "result": worst_result.result if worst_result else "",
                },
                "session_count": player_data.session_count,
                "recent_sessions": recent_sessions,
                "script_id": script_id,
            }
        )
    return render(request, "home/top_players.html", {"top_players": top_players})


def sessions_list(request):
    """Render the session history table."""
    sessions = PokerSession.objects.order_by("-date")
    return render(request, "home/sessions.html", {"sessions": sessions})


def hall_of_fame(request):
    players_qs = (
        Player.objects.annotate(
            has_custom_photo=Case(
                When(
                    photo_filename__isnull=False,
                    photo_filename__iexact="anon.jpg",
                    then=Value(0),
                ),
                default=Value(1),
                output_field=IntegerField(),
            )
        )
        .order_by("-has_custom_photo", "id")
    )
    players = list(players_qs)
    for player in players:
        player.description = _clean_desc(player.description)
    return render(request, "home/hall_of_fame.html", {"players": players})


def new_session(request):
    """Interactive page to draft a new session; POST persists to history."""
    if request.method == "POST":
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        if payload.get("password") != "admin1234":
            return HttpResponseForbidden("Invalid password")

        games = payload.get("games", [])
        totals: dict[str, dict] = {}

        for game in games:
            for player_entry in game.get("players", []):
                pid = player_entry.get("id")
                name = player_entry.get("name") or ""
                raw_res = player_entry.get("result", 0)
                try:
                    res_val = Decimal(str(raw_res))
                except Exception:
                    res_val = Decimal("0")

                key = str(pid) if pid is not None else name
                if key not in totals:
                    totals[key] = {"id": pid, "name": name, "total": Decimal("0")}
                totals[key]["total"] += res_val

        players_map: dict[Player, Decimal] = {}
        for entry in totals.values():
            pid = entry["id"]
            name = entry["name"] or "Игрок"
            player = None
            if pid is not None and str(pid).isdigit():
                player = Player.objects.filter(id=int(pid)).first()
            if player is None:
                player, _ = Player.objects.get_or_create(name=name)
            players_map[player] = entry["total"]

        if not players_map:
            return HttpResponseBadRequest("No results to save")

        session = PokerSession.objects.create(date=timezone.now())
        for player, total in players_map.items():
            SessionResult.objects.create(session=session, player=player, result=total)

        return JsonResponse({"ok": True, "session_id": session.id})

    players = list(Player.objects.order_by("name"))
    for p in players:
        p.description = _clean_desc(p.description)
    return render(
        request,
        "home/new_session.html",
        {"players": players, "players_json": json.dumps([{"id": p.id, "name": p.name} for p in players])},
    )


def session_detail(request, pk: int):
    session = get_object_or_404(PokerSession, pk=pk)
    base_results = list(
        SessionResult.objects.filter(session=session).select_related("player")
    )
    profile_data = []
    for result in base_results:
        player = result.player
        player.description = _clean_desc(player.description)
        player_results = (
            SessionResult.objects.filter(player=player)
            .select_related("session")
            .order_by("-session__date")
        )
        player_session_count = player_results.count()
        best_result = player_results.order_by("-result").first()
        worst_result = player_results.order_by("result").first()
        recent_sessions = []
        for recent in player_results[:3]:
            recent_sessions.append(
                {
                    "session_id": recent.session.id,
                    "date": recent.session.date.strftime("%d.%m.%Y"),
                    "result": str(recent.result),
                }
            )
        script_id = f"session-player-{player.id}"
        profile_data.append(
            {
                "result": result,
                "best": best_result,
                "worst": worst_result,
                "recent_sessions": recent_sessions,
                "script_id": script_id,
            }
        )
    return render(
        request,
        "home/session_detail.html",
        {"session": session, "profile_data": profile_data},
    )


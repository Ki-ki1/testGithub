import os
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

# initialise l'environnement Django (adapter le nom si nécessaire)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "firstproject.settings")
django.setup()

# imports des models après setup
from conferenceApp.models import Conference
from sessionApp.models import Session

mcp = FastMCP("Conference Assistant")

# 1) lister toutes les conférences
@mcp.tool()
async def list_conferences() -> str:
    @sync_to_async
    def _get_confs():
        return list(Conference.objects.all())
    conferences = await _get_confs()
    if not conferences:
        return "No conferences found."
    lines = [f"- {c.name} ({c.start_date} to {c.end_date})" for c in conferences]
    return "\n".join(lines)

# 2) détails d'une conférence par nom (approx. match)
@mcp.tool()
async def get_conference_details(name: str) -> str:
    @sync_to_async
    def _get_conf():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
    conf = await _get_conf()
    if conf == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conf:
        return f"Conference '{name}' not found."
    return (
        f"Name: {conf.name}\n"
        f"Theme: {getattr(conf, 'theme', 'N/A')}\n"
        f"Location: {getattr(conf, 'location', 'N/A')}\n"
        f"Dates: {conf.start_date} to {conf.end_date}\n"
        f"Description: {getattr(conf, 'description','')}"
    )

# 3) lister les sessions d'une conférence
@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(conference.sessions.all()), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    result, conference = await _get_sessions()
    if result == "MULTIPLE":
        return f"Multiple conferences found matching '{conference_name}'. Please be more specific."
    if conference is None:
        return f"Conference '{conference_name}' not found."
    sessions = result
    if not sessions:
        return f"No sessions found for conference '{conference.name}'."
    session_lines = []
    for s in sessions:
        session_lines.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n  Topic: {s.topic}"
        )
    return "\n".join(session_lines)

# 4) Tool métier libre : ex. filtrer par thème et/ou date range
@mcp.tool()
async def filter_conferences(theme: str = "", start_after: str = "", end_before: str = "") -> str:
    """
    theme: substring to match theme
    start_after: yyyy-mm-dd
    end_before: yyyy-mm-dd
    """
    from datetime import datetime

    @sync_to_async
    def _filter():
        qs = Conference.objects.all()
        if theme:
            qs = qs.filter(theme__icontains=theme)
        if start_after:
            try:
                d = datetime.fromisoformat(start_after).date()
                qs = qs.filter(start_date__gte=d)
            except Exception:
                pass
        if end_before:
            try:
                d = datetime.fromisoformat(end_before).date()
                qs = qs.filter(end_date__lte=d)
            except Exception:
                pass
        return list(qs)
    confs = await _filter()
    if not confs:
        return "No conferences match the criteria."
    return "\n".join([f"- {c.name} ({c.start_date} to {c.end_date}) - {c.theme}" for c in confs])

if __name__ == "__main__":
    # lance le serveur MCP sur stdio (inspecteur peut s'y connecter)
    mcp.run(transport="stdio")

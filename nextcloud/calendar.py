"""API WebDAV Nextcloud pour la gestion du calendrier."""

from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from caldav.davclient import DAVClient

from config.settings import settings
from utils.logger import logger

EVENT_TITLE = "[AUTO] livres à rendre"


class NextcloudCalendar:
    """Gère la connexion et les opérations sur le calendrier Nextcloud."""

    def __init__(self, timezone: str | None):
        """
        Initialise la connexion au calendrier Nextcloud.

        Raises:
            ValueError: Si CALENDRIER_ID n'est pas spécifié ou introuvable
        """
        if not settings.CALENDRIER_ID:
            raise ValueError("CALENDRIER_ID doit être spécifié dans la configuration")

        self.timezone = ZoneInfo(timezone or settings.TIMEZONE)

        caldav_url = f"{settings.NEXTCLOUD_URL}/remote.php/dav/calendars/{settings.NEXTCLOUD_APP_USER}/"

        self.client = DAVClient(
            url=caldav_url,
            username=settings.NEXTCLOUD_APP_USER,
            password=settings.NEXTCLOUD_APP_PASSWORD,
        )

        principal = self.client.principal()
        calendars = principal.calendars()

        # Trouver le bon calendrier par nom
        self.calendar = next(
            (cal for cal in calendars if cal.id == settings.CALENDRIER_ID), None
        )

        if not self.calendar:
            raise ValueError(f"Calendrier '{settings.CALENDRIER_ID}' introuvable")

    def _get_date_from_str(self, date_str: str):
        """Génère une date depuis une string, en utilisant la bonne timezone"""
        return (
            datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=self.timezone).date()
        )

    def _generate_event_data(self, books: list) -> dict:
        """
        Génère les données pour un événement de rendu de livres.

        Args:
            books: Liste de dictionnaires contenant les informations des livres
            date_str: Date au format YYYY-MM-DD

        Retourne:
            dict: Dictionnaire avec summary, description et dtstart
        """
        count = len(books)
        summary = f"{EVENT_TITLE} ({count})"

        description_lines = ["Livres à rendre à la médiathèque"]
        for book in books:
            desc = f"- {book['title']}"
            if author := book.get("author"):
                desc += f" - {author}"
            if location := book.get("location"):
                desc += f" ({location})"
            description_lines.append(desc)

        description = "\n".join(description_lines)

        return {
            "summary": summary,
            "description": description,
        }

    def create_or_update_event(self, books: list, date_str: str) -> bool:
        """
        Crée ou met à jour un événement pour la date donnée (journée entière).

        Args:
            books: Liste de dictionnaires contenant les informations des livres
            date_str: Date au format YYYY-MM-DD

        Retourne:
            bool: True si l'événement a été créé/mis à jour, False en cas d'erreur
        """
        try:
            event_data = self._generate_event_data(books)

            # On crée un évènement pour la journée entière,
            # il nous faut une date et pas un datetime
            start = self._get_date_from_str(date_str)

            # Add event est idempotent grâce à l'uid
            # Si un évènement existe déjà à cette date, il sera modifié
            self.calendar.add_event(
                summary=event_data["summary"],
                description=event_data["description"],
                dtstart=start,
                dtend=start + timedelta(days=1),  # exclusif
                uid=f"books-due-{start}@{settings.NEXTCLOUD_APP_USER}",
            )
            logger.info(f"[CALENDAR] Événement créé/mis à jour pour le {date_str}")

            return True

        except Exception as e:
            logger.error(f"[CALENDAR] Échec création événement Nextcloud: {str(e)}")
            return False

    def sync_events(self, books: list) -> int:
        """
        Synchronise les événements pour tous les livres.

        Args:
            books: Liste de dictionnaires contenant les informations des livres

        Retourne:
            int: Nombre d'événements créés ou mis à jour
        """
        if not books:
            logger.info("[CALENDAR] Aucun livre à traiter")
            return 0

        # Regrouper les livres par date de rendu
        books_by_date = defaultdict(list)
        for book in books:
            date_str = book["due_date"]
            if date_str:
                books_by_date[date_str].append(book)

        events_count = 0
        for date_str, date_books in books_by_date.items():
            event_created = self.create_or_update_event(date_books, date_str)
            if event_created:
                events_count += 1

        return events_count


def create_events(books: list, timezone: str | None = None) -> int:
    """
    Crée ou met à jour les événements dans le calendrier Nextcloud.

    Args:
        books: Liste de dictionnaires contenant les informations des livres
        timezone: Fuseau horaire (optionnel, par défaut celui de la config)

    Retourne:
        int: Nombre d'événements créés ou mis à jour
    """
    calendar = NextcloudCalendar(timezone)
    return calendar.sync_events(books)

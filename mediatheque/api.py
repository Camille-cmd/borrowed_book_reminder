"""API de récupération des prêts de livres."""

from datetime import datetime

from requests.exceptions import RequestException

from config.settings import settings
from mediatheque.auth import MediathequeAuth
from utils.logger import logger
from utils.utils import get_tzinfo


class MediathequeAPI:
    """Gère les requêtes à l'API de la médiathèque."""

    def __init__(self):
        """
        Initialise l'API.

        Args:
            auth: Instance de MediathequeAuth pour la gestion des cookies
        """
        self.url = settings.MEDIATHEQUE_URL

        # Login
        auth = MediathequeAuth()
        self.auth = auth
        self.auth.login()
        self.session = auth.session

    def get_loans(self) -> list:
        """
        Récupère la liste des prêts de livres.

        Retourne:
            list: Liste de dictionnaires contenant les informations des livres
        """
        try:
            service_url = f"{self.url}/Portal/Services/UserAccountService.svc/ListLoans"

            timestamp = datetime.now().isoformat()

            params = {
                "serviceCode": "SYRACUSE",
                "userUniqueIdentifier": "",
                "timestamp": timestamp,
            }

            logger.info("[API] Tentative de récupération des prêts")

            response = self.session.get(
                service_url, params=params, headers=self.auth.get_headers(), timeout=30
            )

            data = response.json()

            if not data.get("success", False):
                error_msg = data.get("errors", [{}])[0].get("msg", "Erreur inconnue")
                logger.error(f"[API] Erreur API: {error_msg}")
                return []

            if not data:
                logger.warning("[API] Réponse vide de l'API")
                return []

            loans = self._extract_loans(data)
            logger.info(f"[API] {len(loans)} livres récupérés via API")
            for loan in loans:
                logger.info(f"{loan['title']} due on {loan['due_date']}")

            return loans

        except RequestException as e:
            logger.error(f"[API] Erreur de récupération: {str(e)}")
            return []

    def _extract_loans(self, data) -> list:
        """
        Extraire les prêts de la réponse JSON.

        Args:
            data: Données JSON brutes de l'API

        Retourne:
            list: Liste de dictionnaires avec les informations des livres
        """
        loans = []

        if isinstance(data, dict):
            d = data.get("d")
            if not d or not isinstance(d, dict):
                logger.warning(f"[API] 'd' non valide: {type(d)}")
                return []
            loans_data = d.get("Loans", [])
        elif isinstance(data, list):
            loans_data = data
        else:
            logger.error(f"[API] Type de données inattendu: {type(data)}")
            return []

        for loan in loans_data:
            if not isinstance(loan, dict):
                continue

            loan_info = {
                "title": self._get_field(loan, ["Title", "title", "Titre"]),
                "due_date": self._parse_due_date(loan),
                "loan_number": self._get_field(
                    loan, ["LoanNumber", "loanNumber", "NuméroPrêt", "Id"]
                ),
                "author": self._get_field(loan, ["Author", "author", "Auteur"]),
                "publisher": self._get_field(
                    loan, ["Publisher", "publisher", "Éditeur"]
                ),
                "url": self._get_field(loan, ["TitleLink", "titleLink", "Url"]),
                "isbn": self._get_field(loan, ["ISBN", "isbn", "ISBN"]),
                "location": self._get_field(loan, ["Location"]),
                "can_renew": self._get_field(loan, ["CanRenew"]),
            }

            if loan_info["title"]:
                loans.append(loan_info)

        return loans

    def _get_field(self, data, fields):
        """Récupère un champ avec plusieurs noms possibles."""
        for field in fields:
            if field in data and data[field]:
                return data[field]
        return None

    def _parse_due_date(self, loan) -> str:
        """
        Parse la date de rendu du livre.

        Retourne:
            str: Date formatée comme 'YYYY-MM-DD'
        """
        due_date = self._get_field(
            loan,
            [
                "DueDate",
                "dueDate",
                "DateRendu",
                "DateRenduPrévue",
                "DateDeRendu",
                "dateDeRendu",
                "DueDateTime",
                "dueDateTime",
                "WhenBack",
                "whenback",
            ],
        )

        if not due_date:
            return None

        # Format spécial: /Date(1775685600000+0200)/
        if (
            isinstance(due_date, str)
            and due_date.startswith("/Date(")
            and due_date.endswith("/")
        ):
            due_date = due_date[6:-2]  # Enlever /Date() et /
            # Enlever les parenthèses
            if due_date.startswith("(") and due_date.endswith(")"):
                due_date = due_date[1:-1]
            # Extraire timestamp et timezone
            if "+" in due_date:
                timestamp_str, tz_offset = due_date.split("+", 1)
                try:
                    timestamp_sec = (
                        int(timestamp_str) / 1000
                    )  # Millisecondes -> secondes
                    dt = datetime.fromtimestamp(timestamp_sec, tz=get_tzinfo())
                    return dt.strftime("%Y-%m-%d")
                except Exception as e:
                    logger.warning(f"[API] Erreur parsing date: {e}, using fallback")
                    return None

        # Essayer différents formats de date
        formats = [
            "%d/%m/%Y",  # 15/01/2024
            "%Y-%m-%d",  # 2024-01-15
            "%d-%m-%Y",  # 15-01-2024
            "%Y/%m/%d",  # 2024/01/15
            "%d.%m.%Y",  # 15.01.2024
            "%m/%d/%Y",  # 01/15/2024
        ]

        for fmt in formats:
            try:
                parsed_date = datetime.strptime(str(due_date), fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except ValueError:
                continue

        logger.warning(f"[API] Date de rendu non parseable: {due_date}")
        return None

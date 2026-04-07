from datetime import datetime

from config.settings import settings
from mediatheque.api import MediathequeAPI
from nextcloud import create_events
from utils.logger import ensure_log_directory

logger = __import__("utils.logger", fromlist=["logger"]).logger


# Initialisation du logging
ensure_log_directory()

# # # Récupérer les prêts
# api = MediathequeAPI()
# loans = api.get_loans()
# print(loans)

loans = [
    {
        "title": "Internet et libertés : 15 ans de combat de la Quadrature du net / Mathieu Labonde, Lou Malhuret, Benoît Piedallu, Axel Simon",
        "due_date": "2026-04-15",
        "loan_number": "20022282",
        "author": None,
        "publisher": None,
        "url": "https://cataloguebm.villeurbanne.fr/Default/doc/SYRACUSE/4377550/internet-et-libertes-15-ans-de-combat-de-la-quadrature-du-net-mathieu-labonde-lou-malhuret-benoit-pi",
        "isbn": None,
        "location": "Médiathèque du Rize",
        "can_renew": True,
    },
    {
        "title": "Neuromancien / William Gibson",
        "due_date": "2026-04-15",
        "loan_number": "20022283",
        "author": None,
        "publisher": None,
        "url": "https://cataloguebm.villeurbanne.fr/Default/doc/SYRACUSE/4286445/neuromancien-william-gibson",
        "isbn": None,
        "location": "Médiathèque du Rize",
        "can_renew": False,
    },
]


# Filtrer les livres dans le futur
today = datetime.now().strftime("%Y-%m-%d")
future_loans = [
    loan for loan in loans if loan.get("due_date") and loan["due_date"] >= today
]

# Synchroniser les événements
if future_loans:
    events_created = create_events(future_loans, settings.TIMEZONE)
else:
    logger.info("[SYNC] Aucun livre à synchroniser (tous rendus)")

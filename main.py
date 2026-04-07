from datetime import datetime

from config.settings import settings
from mediatheque.api import MediathequeAPI
from nextcloud import create_events
from utils.logger import ensure_log_directory

logger = __import__("utils.logger", fromlist=["logger"]).logger

# Initialisation du logging
ensure_log_directory()

# Récupérer les prêts
api = MediathequeAPI()
loans = api.get_loans()

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

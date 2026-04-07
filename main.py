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

# Synchroniser les événements
create_events(loans, settings.TIMEZONE)

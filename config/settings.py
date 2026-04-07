"""Chargement et validation de la configuration."""

import os

from dotenv import load_dotenv

from utils.logger import logger


def load_config():
    """
    Charge la configuration depuis les variables d'environnement.

    Retourne:
        Namespace: Objet contenant toutes les variables de configuration
    """
    load_dotenv()

    config = {
        # Médiathèque
        "MEDIATHEQUE_URL": os.getenv(
            "MEDIATHEQUE_URL", "https://cataloguebm.villeurbanne.fr"
        ),
        "MEDIATHEQUE_USER": os.getenv("MEDIATHEQUE_USER"),
        "MEDIATHEQUE_PASS": os.getenv("MEDIATHEQUE_PASS"),
        # Nextcloud
        "NEXTCLOUD_URL": os.getenv("NEXTCLOUD_URL"),
        "NEXTCLOUD_APP_USER": os.getenv("NEXTCLOUD_APP_USER"),
        "NEXTCLOUD_APP_PASSWORD": os.getenv("NEXTCLOUD_APP_PASSWORD"),
        # Calendrier
        "CALENDRIER_ID": os.getenv("CALENDRIER_ID"),
        # Système
        "TIMEZONE": os.getenv("TIMEZONE", "Europe/Paris"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
    }

    # Validation des variables critiques
    missing_vars = []
    if not config["MEDIATHEQUE_USER"]:
        missing_vars.append("MEDIATHEQUE_USER")
    if not config["MEDIATHEQUE_PASS"]:
        missing_vars.append("MEDIATHEQUE_PASS")

    if missing_vars:
        logger.error(f"Configuration manquante: {', '.join(missing_vars)}")
        raise ValueError(
            f"Variables d'environnement manquantes: {', '.join(missing_vars)}"
        )

    class Settings:
        def __init__(self, data):
            for key, value in data.items():
                setattr(self, key, value)

    return Settings(config)


settings = load_config()

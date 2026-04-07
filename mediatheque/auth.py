"""Authentification API de la médiathèque Villeurbanne."""

import requests
from requests.exceptions import RequestException

from config.settings import settings
from utils.logger import logger


class MediathequeAuth:
    """Gère la connexion à l'API de la médiathèque."""

    def __init__(self):
        """Initialise l'authentification avec l'URL de la médiathèque."""
        self.url = settings.MEDIATHEQUE_URL
        self.session = requests.Session()
        self.cookies = {}

    def login(self) -> bool:
        """
        Se connecte à l'API de la médiathèque.

        Retourne:
            bool: True si la connexion réussit, False sinon
        """
        try:
            logon_url = f"{self.url}/Portal/Recherche/logon.svc/logon"

            payload = {
                "username": settings.MEDIATHEQUE_USER,
                "password": settings.MEDIATHEQUE_PASS,
                "rememberMe": "false",
            }

            headers = {
                "Referer": f"{self.url}/",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            logger.info("[CONNECT] Tentative de connexion à la médiathèque")

            response = self.session.post(
                logon_url, data=payload, headers=headers, timeout=30
            )

            response.raise_for_status()

            self.cookies = response.cookies.get_dict()

            if not self.cookies:
                logger.warning("[CONNECT] Aucune cookie reçu, vérification du succès")
                if response.status_code == 200:
                    logger.info("[CONNECT] Connexion réussie (aucun cookie stocké)")
                    return True
                else:
                    logger.error(
                        f"[CONNECT] Erreur de connexion: {response.status_code}"
                    )
                    return False

            logger.info("[CONNECT] Connexion médiathèque réussie")

            return True

        except RequestException as e:
            logger.error(f"[CONNECT] Erreur de connexion: {str(e)}")
            return False

    def get_headers(self) -> dict:
        """Retourne les headers avec les cookies de session."""
        headers = {"Referer": f"{self.url}/"}
        if self.cookies:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())
        return headers

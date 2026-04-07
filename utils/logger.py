"""Configuration et gestion du logging."""

import os
from logging import basicConfig, getLogger


def setup_logger(log_level: str = "INFO") -> getLogger:
    """
    Configure le logging pour le projet.

    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR)

    Retourne:
        Logger: Instance de logger configurée
    """
    basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=log_level.upper(),
        filename="logs/app.log",
        filemode="a",
    )

    logger = getLogger(__name__)

    return logger


logger = setup_logger()


def ensure_log_directory():
    """Crée le dossier logs s'il n'existe pas."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        logger.info(f"Dossier logs créé: {log_dir}")

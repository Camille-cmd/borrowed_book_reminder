"""Configuration et gestion du logging."""

import os
import sys
from datetime import datetime
from logging import getLogger, basicConfig, INFO, DEBUG, WARNING, ERROR


def setup_logger(log_level="INFO") -> getLogger:
    """
    Configure le logging pour le projet.

    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR)

    Retourne:
        Logger: Instance de logger configurée
    """
    log_levels = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR
    }

    level = log_levels.get(log_level.upper(), INFO)

    basicConfig(
        format="%(message)s",
        level=level
    )

    logger = getLogger(__name__)

    return logger


logger = setup_logger()


def get_log_file_name():
    """
    Génère le nom du fichier de log actuel.

    Retourne:
        str: Nom du fichier de log (logs/sync_{DATE}.log)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return f"logs/sync_{today}.log"


def ensure_log_directory():
    """Crée le dossier logs s'il n'existe pas."""
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        logger.info(f"Dossier logs créé: {log_dir}")

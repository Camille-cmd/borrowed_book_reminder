[![Language: English](https://img.shields.io/badge/Langue-English-blue.svg)](README.md)

# Synchronisation Médiathèque Villeurbanne → Nextcloud

Script Python automatisé qui synchronise les livres empruntés de la médiathèque de Villeurbanne vers le calendrier Nextcloud.

## Fonctionnalités

- Récupération automatique des prêts de livres via l'API de la médiathèque
- Création et mise à jour d'événements dans Nextcloud via WebDAV
- Groupement des livres par date de rendu
- Gestion des renouvellements
- Journalisation complète

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (package manager)

## Installation

```bash
# Créer l'environnement virtuel
uv venv

# Activer l'environnement
source .venv/bin/activate  # Linux/macOS

# Installer les dépendances
uv sync
```

## Configuration

Créez un fichier `.env` à la racine du projet :

```bash
MEDIATHEQUE_URL=https://cataloguebm.villeurbanne.fr
MEDIATHEQUE_USER=votre_utilisateur
MEDIATHEQUE_PASS=votre_mot_de_passe

NEXTCLOUD_URL=https://nextcloud.votre-domaine.fr
NEXTCLOUD_APP_USER=votre_utilisateur
NEXTCLOUD_APP_PASSWORD=votre_mot_de_passe_application

TIMEZONE=Europe/Paris
```

## Lancement

```bash
uv run main.py
```

## Cron Job

Pour exécuter automatiquement le script, ajoutez cette ligne dans `crontab` (`crontab -e`) :

```bash
0 8 * * * cd /chemin/vers/le/projet && uv run main.py >> logs/cron.log 2>&1
```

## License

Ce projet est distribué sous licence GNU GPL v3.0 - voir le fichier LICENSE.md pour plus de détails.

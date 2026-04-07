[![Language: French](https://img.shields.io/badge/Language-Français-green.svg)](README-FR.md)

# Borrowed Book Reminder - Villeurbanne Library to Nextcloud Sync

Automated Python script that synchronizes borrowed books from the Villeurbanne public library to your Nextcloud calendar.

## Features

- Automatically retrieves borrowed books via the library's REST API
- Creates and updates calendar events in Nextcloud via WebDAV
- Groups books by due date
- Handles book renewals
- Comprehensive logging

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (package manager)

## Installation

```bash
# Create virtual environment
uv venv

# Activate the environment
source .venv/bin/activate  # Linux/macOS

# Install dependencies
uv sync
```

## Configuration

Create a `.env` file in the project root:

```bash
MEDIATHEQUE_URL=https://cataloguebm.villeurbanne.fr
MEDIATHEQUE_USER=your_username
MEDIATHEQUE_PASS=your_password

NEXTCLOUD_URL=https://nextcloud.your-domain.com
NEXTCLOUD_APP_USER=your_username
NEXTCLOUD_APP_PASSWORD=your_app_password

TIMEZONE=Europe/Paris
```

## Usage

```bash
uv run main.py
```

## Cron Job

To run the script automatically, add this line to your `crontab` (`crontab -e`):

```bash
0 8 * * * cd /path/to/project && uv run main.py >> logs/cron.log 2>&1
```

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE.md file for details

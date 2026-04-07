from zoneinfo import ZoneInfo

from config.settings import settings


def get_tzinfo(timezone: str | None = None) -> ZoneInfo:
    """Retourne la timezone sous forme de class ZoneInfo"""
    return ZoneInfo(timezone or settings.TIMEZONE)

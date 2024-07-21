from datetime import datetime

from typing import Optional

DATETIME_FORMATS = [
    "%Y%m%d%H%M%S",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%dT%H:%M",
]

def parse_datetime(raw_datetime: str, raise_exception=False) -> Optional[datetime]:
    raw_datetime = raw_datetime.strip()
    parsed_datetime = None
    for fmt in DATETIME_FORMATS:
        try:
            parsed_datetime = datetime.strptime(raw_datetime, fmt)
        except ValueError:
            pass
    if raise_exception and parse_datetime is None:
        raise ValueError(f"Could not parse {raw_datetime} to datetime!")
    return parsed_datetime
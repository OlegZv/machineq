import warnings
from datetime import datetime, timezone


def ensure_utc_and_str(dt: datetime) -> str:
    """Ensure a datetime is timezone-aware in timezone.utc.
    If the user provides a naive datetime, issue a warning and try our best to convert from local
    timezone to timezone.utc. If the user provides a timezone-aware datetime, convert it to timezone.utc if it's not already.
    """
    if dt.tzinfo is None:
        # Naive datetime, assume it's in local timezone and convert to timezone.utc

        warnings.warn(
            "Naive datetime provided. Assuming local timezone and converting to timezone.utc. "
            "Please provide timezone-aware datetimes in the future.",
            UserWarning,
            stacklevel=2,
        )
        dt = dt.astimezone(timezone.utc)
    else:
        # Timezone-aware datetime, convert to timezone.utc if it's not already
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")

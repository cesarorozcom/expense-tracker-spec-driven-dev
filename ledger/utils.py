"""
Utilities for timezone-aware operations in recurring transaction management.

Provides helpers for:
- Converting between local and UTC timestamps
- Determining the next occurrence of a recurring event
- Handling timezone-aware datetime calculations for recurring rules
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pytz


def get_utc_now():
    """Return current time in UTC (timezone-aware)."""
    return datetime.now(ZoneInfo("UTC"))


def make_aware_in_timezone(dt, tz_name="UTC"):
    """
    Make a naive datetime timezone-aware in the specified timezone.
    
    Args:
        dt: naive datetime object
        tz_name: timezone name (e.g., 'UTC', 'America/New_York', 'Europe/London')
    
    Returns:
        timezone-aware datetime object
    """
    if dt.tzinfo is not None:
        return dt  # Already timezone-aware
    
    try:
        tz = ZoneInfo(tz_name)
    except KeyError:
        # Fallback to pytz if zoneinfo doesn't recognize the timezone
        tz = pytz.timezone(tz_name)
    
    return dt.replace(tzinfo=tz)


def convert_to_timezone(dt, tz_name="UTC"):
    """
    Convert a timezone-aware datetime to a different timezone.
    
    Args:
        dt: timezone-aware datetime object
        tz_name: target timezone name
    
    Returns:
        datetime object in the target timezone
    """
    if dt.tzinfo is None:
        raise ValueError("datetime must be timezone-aware")
    
    try:
        tz = ZoneInfo(tz_name)
    except KeyError:
        tz = pytz.timezone(tz_name)
    
    return dt.astimezone(tz)


def get_next_occurrence(base_date, frequency, interval=1, tz_name="UTC"):
    """
    Calculate the next occurrence of a recurring event.
    
    Args:
        base_date: starting date (datetime or date object)
        frequency: 'daily', 'weekly', 'biweekly', 'monthly', 'quarterly', 'yearly'
        interval: number of periods to add (default: 1)
        tz_name: timezone for calculation (default: 'UTC')
    
    Returns:
        next occurrence as datetime in specified timezone
    """
    if isinstance(base_date, datetime):
        dt = base_date
    else:
        # Convert date to datetime at midnight in the specified timezone
        dt = datetime.combine(base_date, datetime.min.time())
        dt = make_aware_in_timezone(dt, tz_name)
    
    frequency_map = {
        'daily': timedelta(days=interval),
        'weekly': timedelta(weeks=interval),
        'biweekly': timedelta(weeks=2 * interval),
        'monthly': None,  # Handled specially below
        'quarterly': None,  # Handled specially below
        'yearly': None,  # Handled specially below
    }
    
    if frequency in ('monthly', 'quarterly', 'yearly'):
        # Use dateutil.relativedelta for month/year arithmetic
        from dateutil.relativedelta import relativedelta
        if frequency == 'monthly':
            delta = relativedelta(months=interval)
        elif frequency == 'quarterly':
            delta = relativedelta(months=3 * interval)
        else:  # yearly
            delta = relativedelta(years=interval)
        next_dt = dt + delta
    else:
        delta = frequency_map.get(frequency)
        if delta is None:
            raise ValueError(f"Unknown frequency: {frequency}")
        next_dt = dt + delta
    
    return next_dt


def is_recurring_due(next_occurrence, as_of=None):
    """
    Check if a recurring transaction is due as of a given time.
    
    Args:
        next_occurrence: next scheduled occurrence (datetime, timezone-aware)
        as_of: reference time (default: now in UTC)
    
    Returns:
        True if next_occurrence is <= as_of
    """
    if as_of is None:
        as_of = get_utc_now()
    
    if next_occurrence.tzinfo is None:
        raise ValueError("next_occurrence must be timezone-aware")
    
    # Normalize both to UTC for comparison
    next_utc = convert_to_timezone(next_occurrence, "UTC")
    as_of_utc = convert_to_timezone(as_of, "UTC") if as_of.tzinfo else make_aware_in_timezone(as_of, "UTC")
    
    return next_utc <= as_of_utc

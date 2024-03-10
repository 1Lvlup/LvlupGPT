from datetime import datetime

def get_current_datetime() -> str:
    """Return the current date and time as a formatted string.

    Returns:
        str: The current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return f"Current date and time: {formatted_datetime}"


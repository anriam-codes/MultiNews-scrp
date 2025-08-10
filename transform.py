from datetime import datetime

def normalize_date(date_str):
    formats = [
        "%b %d, %Y %I:%M %p IST",  # Aug 07, 2025 01:22 PM IST
        "%b %d, %Y %H:%M %p IST",  # Aug 07, 2025 13:22 pm IST (odd format)
        "%b %d, %Y",               # Aug 07, 2025
        "%Y-%m-%d"                 # 2025-08-07
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str

from typing import Union
from datetime import datetime, date
from urllib.parse import urlparse

def get_message(update) -> Union[str, None]:
    if "message" not in update:
        return None

    if "text" in update["message"]:
        return update["message"]["text"]
    
    return None

def get_message_id(update):
    if "message" not in update:
        return None

    if "text" in update["message"]:
        return update["message"]["message_id"]
    else:
        return None

def get_user_id(update) -> Union[str, int]:
    if "message" in update:
        return update["message"]["from"]["id"]
    elif "callback_query" in update:
        return update["callback_query"]["from"]["id"]
    return 0


def get_callback_message_id(update):
    if "callback_query" in update:
        return update["callback_query"]["message"]["message_id"]
    else:
        return None

def get_callback_text(update):
    if "callback_query" in update:
        if "text" in update["callback_query"]["message"]:
            return update["callback_query"]["message"]["text"]
        else:
            return None
    else:
        return None

def get_callback_data(update):
    if "callback_query" in update:
        return update["callback_query"]["data"]
    else:
        return None
    
def is_date_available(date: Union[str, None]) -> Union[bool, date]:
    if date is None:
        return False
    
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return False
    
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

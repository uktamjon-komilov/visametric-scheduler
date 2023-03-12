from django.conf import settings
import requests as r
import json


BASE_URL = "https://api.telegram.org/bot{}/".format(settings.BOT_TOKEN)


def bot(method, data):
    response = r.post(BASE_URL + method, json=data)
    return json.loads(response.text)


def send_message(text, chat_id, menu = None, parse_mode = "html"):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }

    if menu:
        data["reply_markup"] = menu
    
    return bot("sendMessage", data)


def edit_message(text, chat_id, message_id, menu = None, parse_mode = "html"):
    data = {
        "chat_id": chat_id,
        "text": text,
        "message_id": message_id,
        "parse_mode": parse_mode
    }

    if menu:
        data["reply_markup"] = menu
    
    return bot("editMessageText", data)


def edit_reply_markup(chat_id, message_id, menu):
    data = {
        "chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": menu
    }

    return bot("editMessageReplyMarkup", data)


def delete_message(chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    return bot("deleteMessage", data)



def send_file(file_url: str, chat_id, parse_mode = "html"):
    data = {
        "chat_id": chat_id,
        "document": file_url,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    
    return bot("sendDocument", data)
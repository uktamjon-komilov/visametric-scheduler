from visametric_bot.models import Customer
from ..constants import *
def main_menu_keyboards():
    MAIN_MENU_BTNS = {
        "inline_keyboard":[
            [
                {"text": EXPRESS_VISA, "callback_data": EXPRESS_VISA_CALLBACK},
                {"text": MONTHLY_VISA, "callback_data": MONTHLY_VISA_CALLBACK},
            ]
        ]
    }
    
    return MAIN_MENU_BTNS

def navigation_keyboards():
    NAVIGATION_BTNS = {
        "inline_keyboard":[
            [
                {"text": TURN_ON, "callback_data": TURN_ON_CALLBACK_DATA},
                {"text": ADD_CLIENT, "callback_data": ADD_CLIENT_CALLBACK_DATA},
            ],
            [
                {"text": CLIENTS, "callback_data": CLIENTS_CALLBACK_DATA}
            ]
        ]
    }
    
    return NAVIGATION_BTNS

def get_clients(plan="monthly", back_btn=False, back_to=None, for_registering=False, add_next_btn=False):
    markup = []
    if for_registering:
        clients = Customer.objects.filter(is_active=True, is_registered=False)
        if len(clients)>0:
            
            for client in clients:
                markup.append(
                    [
                        {"text": client.get_full_name(), "callback_data": f"{client.pk}"},
                        {"text": "✅", "callback_data": f"action:add_to_register-{client.pk}"},
                    ]
                    
                )
        elif add_next_btn or len(clients) == 0:
            markup.append(
                [
                    {"text": "Yakunlash", "callback_data": "finish_registering"}
                ]
            )
    else:
        clients = Customer.get_all_customers(plan="monthly")
        for client in clients:
            markup.append(
                [
                    {"text": client.get_full_name(), "callback_data": f"{client.pk}"},
                    {"text": "✏️", "callback_data": f"action:edit-{client.pk}"},
                    {"text": "❌", "callback_data": f"action:remove-{client.pk}"},
                ]
                
            )

    return {
        "inline_keyboard":markup
    }
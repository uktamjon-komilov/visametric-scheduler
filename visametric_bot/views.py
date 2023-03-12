import json
from datetime import datetime, date

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Customer, User
from .scraper import WebScraper
from .bot import (
    send_message,
    delete_message
)
from .helpers import (
    get_callback_data,
    get_callback_message_id,
    get_message,
    get_user_id,
    is_date_available
)
from .keyboards.inline import main_menu_keyboards, navigation_keyboards, get_clients
from .keyboards.default import get_address_keyboards
from .constants import (
    EXPRESS_VISA_CALLBACK,
    MONTHLY_VISA_CALLBACK,
    ADD_CLIENT_CALLBACK_DATA,
    ADDRESS_OPTIONS,
    CLIENTS_CALLBACK_DATA,
    TURN_ON_CALLBACK_DATA
)
from .tasks import check_availibility, fill_form

user_data = {}
notification = False

@csrf_exempt
def main(request):

    if request.method == "GET":
        return HttpResponse("Salom")

    update = json.loads(request.body)

    user_id = get_user_id(update)
    message = get_message(update)
    callback_message_id = get_callback_message_id(update)
    callback_data = get_callback_data(update)
    if not callback_data:
        callback_data = ""

    state = User.get_state(user_id)

    if message == "/start" or callback_data == "back_to_main_menu":
        send_message(
            text="welcome to the bot!",
            chat_id=user_id,
            menu=main_menu_keyboards()
        )
        User.set_state(user_id, "start")

    elif state == "start" and callback_data == EXPRESS_VISA_CALLBACK:
        delete_message(user_id, callback_message_id)
        send_message(
            "this part of the bot is under the development",
            user_id
        )

    elif state == "start" and callback_data == MONTHLY_VISA_CALLBACK:
        delete_message(user_id, callback_message_id)
        send_message(
            "Action list:",
            user_id,
            navigation_keyboards()
        )
        User.set_state(user_id, "monthly_plan")

    elif state == "monthly_plan" and callback_data == ADD_CLIENT_CALLBACK_DATA:
        delete_message(user_id, callback_message_id)
        send_message(
            "Klient ismini kiriting:\nRo'yxatdan o'tishni to'xtatish uchun /cancel_reg commandasini yozing",
            user_id,
        )
        User.set_state(user_id, "get_first_name")

    elif state == "get_first_name":
        user_data["first_name"] = message
        send_message(
            "Klient familiyasini kiriting:",
            user_id,
        )
        User.set_state(user_id, "get_last_name")

    elif state == "get_last_name":
        user_data["last_name"] = message
        send_message(
            "Klientning passport raqamini kiriting: *7 raqamdan iborat bo'lishi kerak*",
            user_id,
            parse_mode="MarkdownV2",
        )
        User.set_state(user_id, "get_passport_number")

    elif state == "get_passport_number":
        if message is not None and len(message) == 7 and message.isdigit():
            user_data["passport_number"] = message
            send_message(
                text="Klientning passport yaroqlilik muddatini kiriting: \n<b>📅 Yil-oy-kun formatida kiriting! Misol: 2035-05-15</b>",
                chat_id=user_id
            )
            User.set_state(user_id, "get_passport_valid_date")
        else:
            send_message(
                text="Passport raqamining o'zini kiritishingiz yetarli bo'ladi\nNamuna: 1234567",
                chat_id=user_id
            )

    elif state == "get_passport_valid_date":
        passport_valid_date = is_date_available(message)
        if not passport_valid_date:
            send_message(chat_id=user_id, text="No to'g'ri format🤦‍♂️ qaytadan shu formatda yozing 'YYYY-MM-DD' iltimoss.")
        
        if (isinstance(passport_valid_date, date) and
            passport_valid_date < datetime.now().date()):
            send_message(chat_id=user_id, text="Passport yaroqlilik muddati kelajakda bo'lishi kerak")
        else:
            user_data["passport_valid_date"] = passport_valid_date
            send_message(
                text='🇺🇳 Klient millatini tanlang:',
                chat_id=user_id,
                menu=get_address_keyboards(get_nationality=True)
            )
            User.set_state(user_id, "get_nationality")

    elif state == "get_nationality":
        user_data["nationality"] = message
        send_message(
            text='📍 Klient addressini tanlang:',
            chat_id=user_id,
            menu=get_address_keyboards()
        )
        User.set_state(user_id, "get_address")

    elif state == "get_address":
        if message not in [address[0] for address in ADDRESS_OPTIONS]:
            send_message(
                text="Mavjud bo'lmagan manzil tanlandi!",
                chat_id=user_id
            )
        else:
            user_data["address"] = message
            send_message(
                text="Client tug'ilgan sanasini kiriting:\n<b>Yil-oy-kun shu formatda kiriting!!!</b>",
                chat_id=user_id
            )
            User.set_state(user_id, "get_birth_date")

    elif state == "get_birth_date":
        birth_date = is_date_available(message)
        if not birth_date:
            send_message(
                text="No to'g'ri sana kiritildi. <b>Yil-oy-kun formatida sana kiriting</b>",
                chat_id=user_id
            )

        if isinstance(birth_date, date) and birth_date > datetime.now().date():
            send_message(
                text="Klient kamida 18 yoshda bo'lishi kerak !!!",
                chat_id=user_id
            )

        user_data["birth_date"] = birth_date
        send_message(
            text='Client emailini kiriting:',
            chat_id=user_id
            )
        
        User.set_state(user_id, "get_email")

    elif state == "get_email":
        user_data['email'] = message
        send_message(
            text='Klient telefon raqamini kiriting:\n998901234567 shu shaklda !!!',
            chat_id=user_id
        )
        User.set_state(user_id, "get_phone_number")

    elif state == "get_phone_number":
        user_data["phone_number"] = message
        Customer(**user_data).save()

        send_message(
            text="Klient muvaffaqiyatli ro'yxatdan o'tkazildi !",
            chat_id=user_id,
            menu=navigation_keyboards()
        )
        User.set_state(user_id, "monthly_plan")

    elif state == "monthly_plan" and callback_data == CLIENTS_CALLBACK_DATA:
        send_message(
            text="Klientlar ro'yxati:\n✏️ -> klient ma'lumorlarini o'zgartirush uchun\n❌ -> Klient ma'lumotlarini databasedan o'chirib yuborish uchun",
            chat_id=user_id,
            menu=get_clients()
        )

    elif callback_data == TURN_ON_CALLBACK_DATA:
        customer = Customer.objects.last()
        if customer is None:
            send_message(
                text="Bazada mijoz mavjud emas!",
                chat_id=user_id
            )
        else:
            check_availibility.delay(customer.id, user_id) # type: ignore
            send_message(
                text="Tekshirilmoqda...",
                chat_id=user_id
            )

    elif callback_data.startswith("action"):
        action = callback_data.split(":")[1].split("-")
        delete_message(user_id, callback_message_id)
        if action[0] == "remove":
            Customer.remove_customer(pk=action[1])
            send_message(
                text="Klient muvaffaqiyatli o'chirildi",
                chat_id=user_id,
                menu=get_clients()
            )
        
        elif action[0] == "edit":
            pass

        elif action[0] == "add_to_register":
            customer = Customer.objects.filter(pk=action[1]).first()
            Customer.edit(customer, "is_registered", True)
            send_message(
                text="Klient muvaffaqiyatli ro'yhatga olish uchun qo'shildi",
                chat_id=user_id,
                menu=get_clients(for_registering=True, add_next_btn=True)
            )

    elif callback_data == "finish_registering":
        customers = Customer.objects.filter(is_active=True, is_registered=True)

        if customers.exists():
            send_message(
                text="Klientlar ro'yhatga olina boshladi :)",
                chat_id=user_id,
            )
            for customer in customers:
                fill_form.delay(customer.id, user_id) # type: ignore
        else:
            send_message(
                text="Mijozlar mavjud emas!",
                chat_id=user_id,
            )

        User.set_state(user_id, "start")

    return HttpResponse("bot is working fine")

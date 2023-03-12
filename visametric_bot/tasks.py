from visametric_bot.scraper import WebScraper
from visametric_bot.models import Customer
from visametric_bot.bot import send_message, send_file
from visametric_bot.keyboards.inline import get_clients
from config.celery import app


@app.task()
def test_celery():
    print("working")

@app.task()
def send_notification():
    customer = Customer.objects.last()

    if customer is None:
        return

    obj = WebScraper(customer)
    if obj.check_availability():
        send_message(
            "Schengen visaga bo'sh joy ochildi 👌",
            1535815443,
        )
    else:
        send_message(
            "Schengen visaga bo'sh joy ochilmagan 😕",
            1535815443,
        )
    
    del obj

@app.task()
def check_availibility(customer_id, user_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        send_message(
            text="Mijoz mavjud emas",
            chat_id=user_id,
            menu=get_clients(for_registering=True)
        )
        return

    scraper = WebScraper(customer)
    if scraper.check_availability():
        send_message(
            text="Ro'yhatga olmoqchi bo'lgan klientlaringizni tanlang",
            chat_id=user_id,
            menu=get_clients(for_registering=True)
        )
    else:
        send_message(
            text="Hozirda VISA uchun bo'sh joylar yo'q",
            chat_id=user_id,
            menu=get_clients(for_registering=True)
        )
    del scraper


@app.task()
def fill_form(customer_id: int, user_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        send_message(
            text="Mijoz mavjud emas",
            chat_id=user_id,
            menu=get_clients(for_registering=True)
        )
        return

    scraper = WebScraper(customer)

    try:
        scraper.fill_form()
        send_message(
            text="Mijoz - {} ro'yhatga olindi!".format(str(customer)),
            chat_id=user_id,
            menu=get_clients(for_registering=True)
        )
        send_file(str(customer.url_for_document), user_id)
    except Exception:
        send_message(
            text="Mijoz - {}ni ro'yhatga olishda muammo mavjud".format(str(customer)),
            chat_id=user_id,
            menu=get_clients(for_registering=True)
        )

    del scraper

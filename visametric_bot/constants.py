USER_STATES = [
    ("start", "start"),
    ("monthly_plan", "monthly plan"),
    ("express_plan", "express plan"),
    ("get_first_name", "get first name"),
    ("get_last_name", "get last name"),
    ("get_passport_number", "get passport number"),
    ("get_passport_valid_date", "get passport valid date"),
    ("get_nationality", "get nationality"),
    ("get_address", "get address"),
    ("get_birth_date", "get birth date"),
    ("get_email", "get email"),
    ("get_phone_number", "get phone number"),
    ("edit_first_name", "edit first name"),
    ("edit_last_name", "edit last name"),
    ("edit_passport_number", "edit passport number"),
    ("edit_passport_valid_date", "edit passport valid date"),
    ("edit_nationality", "edit nationality"),
    ("edit_address", "edit address"),
    ("edit_birth_date", "edit birth date"),
    ("edit_email", "edit email"),
    ("edit_phone_number", "edit phone number"),
]

TURN_ON = "▶️ Visani yoqish"
ADD_CLIENT = "➕ Klient qo'shish"
CLIENTS = "🙍‍♂️ Klientlarni ko'rish"

TURN_ON_CALLBACK_DATA = "turn_on_monthly_visa"
ADD_CLIENT_CALLBACK_DATA = "add_client"
CLIENTS_CALLBACK_DATA = "clients"

PLANS = [
    ("monthly", "Monthly"),
    ("express", "Express"),
]

ADDRESS_OPTIONS = [
    ("Andijan", "Andijan"),
    ("Angren", "Angren"),
    ("Bekobod", "Bekobod"),
    ("Bukhara", "Bukhara"),
    ("Chirchiq", "Chirchiq"),
    ("Fergana", "Fergana"),
    ("Jizzakh", "Jizzakh"),
    ("Kokand", "Kokand"),
    ("Margilan", "Margilan"),
    ("Namangan", "Namangan"),
    ("Navoiy", "Navoiy"),
    ("Nukus", "Nukus"),
    ("Olmaliq", "Olmaliq"),
    ("Qarshi", "Qarshi"),
    ("Samarkand", "Samarkand"),
    ("Shahrisabz", "Shahrisabz"),
    ("Tashkent", "Tashkent"),
    ("Termez", "Termez"),
    ("Urgench", "Urgench"),
]

NATIONALITY_OPTIONS = [
    ("Uzbekistan", "Uzbekistan"),
    ("Special", "Special"),
    ("Foreign", "Foreign"),
]

EXPRESS_VISA = "Express Visa"
MONTHLY_VISA = "Oylik Visa"
EXPRESS_VISA_CALLBACK = "express_visa"
MONTHLY_VISA_CALLBACK = "monthly_visa"

fields = {
    "first_name": "Ism",
    "last_name": "Familiya",
    "email": "email",
    "nationality": "Millati",
    "address": "Manzili",
    "passport_number": "Passport raqami",
    "phone_number": "Telefon raqami",
    "birth_date": "Tug'ilgan sanasi",
    "passport_valid_date": "Passport yaroqlilik muddati"
}
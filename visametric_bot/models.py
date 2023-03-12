from __future__ import annotations

from typing import Union, List
from django.db import models

from .constants import (
    NATIONALITY_OPTIONS,
    ADDRESS_OPTIONS,
    USER_STATES,
    PLANS
)

class User(models.Model):
    telegram_id = models.CharField(max_length=20, unique=True)
    state = models.CharField(max_length=35, choices=USER_STATES)

    @staticmethod
    def get_state(user_id: Union[str, int]) -> Union[str, None]:
        user = User.objects.filter(telegram_id=user_id).first()
        if user is None:
            return None
        return user.state

    @staticmethod
    def set_state(user_id: Union[str, int], state: str) -> None:
        user, _ = User.objects.get_or_create(telegram_id=str(user_id))
        user.state = state
        user.save()


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    nationality = models.CharField(max_length=25, choices=NATIONALITY_OPTIONS)
    address = models.CharField(max_length=25, choices=ADDRESS_OPTIONS)
    passport_number = models.CharField(max_length=25)
    phone_number = models.CharField(max_length=12)
    plan = models.CharField(max_length=20, choices=PLANS, default="monthly")
    birth_date = models.DateField()
    passport_valid_date = models.DateField()
    is_registered = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    url_for_document = models.CharField(max_length=500, blank=True, null=True)

    
    def get_full_name(self) -> str:
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)
    
    def __str__(self) -> str:
        return self.get_full_name()
    
    @staticmethod
    def remove_customer(pk: Union[str, int]):
        try:
            customer = Customer.objects.filter(id=pk).first()
            if customer is not None:
                customer.delete()
        except Exception:
            pass

    @staticmethod
    def get_all_customers(plan: str) -> List[Customer]:
        return list(Customer.objects.filter(plan=plan))

    @staticmethod
    def edit(customer: Union[Customer, int, str, None], field, value):
        if isinstance(customer, Customer):
            setattr(customer, field, value)
            customer.save()
        elif isinstance(customer, int) or isinstance(customer, str):
            instance = Customer.objects.filter(id=customer).first()
            if instance is None:
                return
            setattr(instance, field, value)
            instance.save()
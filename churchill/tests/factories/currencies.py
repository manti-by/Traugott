import factory
from factory.django import DjangoModelFactory

from churchill.apps.currencies.models import Currency


class CurrencyFactory(DjangoModelFactory):
    class Meta:
        model = Currency

    name = factory.Faker("currency_name")
    iso3 = factory.Faker("currency_code")

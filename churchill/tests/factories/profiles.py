import random
import factory.fuzzy
from django.conf import settings
from factory.django import DjangoModelFactory, ImageField

from churchill.apps.profiles.models import Profile
from churchill.tests.factories.currencies import CurrencyFactory


class ProfileDictFactory(factory.Factory):
    class Meta:
        model = dict

    email = factory.Faker("email")
    language = factory.fuzzy.FuzzyChoice(settings.LANGUAGES, lambda x: x[0])
    currency = factory.Faker("currency_code")
    avg_consumption = factory.Faker("pyint", min_value=3000, max_value=10000)
    avg_price = factory.Faker(
        "pydecimal",
        left_digits=5,
        right_digits=2,
        positive=True,
        min_value=5,
        max_value=25,
    )

    @factory.post_generation
    def companies(self, create, extracted, *args, **kwargs):
        self["currency"] = CurrencyFactory(iso3=self["currency"]).iso3


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    image = ImageField(width=800, height=600)
    language = factory.fuzzy.FuzzyChoice(settings.LANGUAGES, lambda x: x[0])
    currency = factory.SubFactory(
        "churchill.tests.factories.currencies.CurrencyFactory"
    )
    avg_consumption = factory.Faker("pyint", min_value=3000, max_value=10000)
    avg_price = factory.Faker(
        "pydecimal",
        left_digits=5,
        right_digits=2,
        positive=True,
        min_value=5,
        max_value=25,
    )

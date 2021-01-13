import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory

from churchill.tests.factories import DEFAULT_USER_PASSWORD


class UserDictFactory(factory.Factory):
    class Meta:
        model = dict

    email = factory.Faker("email")
    username = factory.LazyAttribute(lambda x: x.email)
    password = DEFAULT_USER_PASSWORD


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    username = factory.LazyAttribute(lambda x: x.email)
    password = factory.PostGenerationMethodCall("set_password", DEFAULT_USER_PASSWORD)
    profile = factory.SubFactory("churchill.tests.factories.profiles.ProfileFactory")

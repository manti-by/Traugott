import factory.fuzzy
from factory.django import DjangoModelFactory

from churchill.apps.shots.models import Shot, ShotItem


class ShotDictFactory(factory.Factory):
    class Meta:
        model = dict

    title = factory.Faker("email")
    volume = factory.Faker("pyint", min_value=50, max_value=500)
    degree = factory.Faker("pyint", min_value=0, max_value=100)
    cost = factory.Faker(
        "pydecimal",
        left_digits=5,
        right_digits=2,
        positive=True,
        min_value=5,
        max_value=25,
    )


class ShotFactory(DjangoModelFactory):
    class Meta:
        model = Shot

    title = factory.Faker("email")
    volume = factory.Faker("pyint", min_value=50, max_value=500)
    degree = factory.Faker("pyint", min_value=0, max_value=100)
    cost = factory.Faker(
        "pydecimal",
        left_digits=5,
        right_digits=2,
        positive=True,
        min_value=5,
        max_value=25,
    )
    created_by = factory.SubFactory("churchill.tests.factories.users.UserFactory")


class ShotItemFactory(DjangoModelFactory):
    class Meta:
        model = ShotItem

    user = factory.SubFactory("churchill.tests.factories.users.UserFactory")
    shot = factory.SubFactory("churchill.tests.factories.shots.ShotFactory")

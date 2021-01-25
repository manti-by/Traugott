import pytest
from django.core import mail
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient
from urllib.parse import urlparse, parse_qsl

from churchill.tests.factories.users import UserFactory


@pytest.mark.django_db
class TestResetPassword:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = UserFactory()

    def test_reset_password(self):
        response = self.client.post(
            reverse("api:v1:user:reset_password"),
            data={"email": self.user.email},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert len(mail.outbox) == 1

        verification_url = urlparse(mail.outbox[0].body)
        reset_password_data = dict(parse_qsl(verification_url.query))
        reset_password_data["password"] = Faker().password(length=8)
        response = self.client.post(
            reverse("api:v1:user:reset_password_confirm"),
            data=reset_password_data,
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

        response = self.client.post(
            reverse("api:v1:user:login"),
            data={
                "email": self.user.email,
                "password": reset_password_data["password"],
            },
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {response.json()['token']}")
        response = self.client.get(reverse("api:v1:profile:profile"))
        assert response.status_code == status.HTTP_200_OK

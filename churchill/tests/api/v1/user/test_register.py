import pytest

from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from urllib.parse import urlparse, parse_qsl

from churchill.tests.factories.users import UserDictFactory


@pytest.mark.django_db
class TestRegister:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user_data = UserDictFactory()

    def test_registration(self):
        response = self.client.post(
            reverse("api:v1:user:register"), data=self.user_data, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert len(mail.outbox) == 1

        verification_url = urlparse(mail.outbox[0].body)
        response = self.client.post(
            reverse("api:v1:user:register_verify"),
            data=dict(parse_qsl(verification_url.query)),
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

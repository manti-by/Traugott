import logging
import requests
import xml.etree.ElementTree as ET

from django.utils.translation import gettext_lazy as _

from churchill.apps.currencies.models import CurrencyValue, Currency, CurrencyValueType

logger = logging.getLogger()


def get_default_currency_id() -> int:
    currency, _ = Currency.objects.get_or_create(
        name="United States Dollar", iso3="USD"
    )
    return currency.id


def get_currency_options() -> dict:
    return {c.iso3: c.name for c in Currency.objects.all()}


def create_currency_pair(currency, node):
    CurrencyValue.objects.create(
        currency=currency,
        type=CurrencyValueType.BUY,
        value=float(node.find("purchase").text),
    )
    CurrencyValue.objects.create(
        currency=currency,
        type=CurrencyValueType.SELL,
        value=float(node.find("sale").text),
    )


def update_currencies():
    byn_currency = Currency.objects.first(iso3="BYN")
    eur_currency = Currency.objects.first(iso3="EUR")
    rub_currency = Currency.objects.first(iso3="RUB")
    if not any((byn_currency, eur_currency, rub_currency)):
        logger.info(_("No currencies are setup"))

    response = requests.get("https://www.mtbank.by/currxml.php?ver=2")
    if response.status_code == 200:
        for child in ET.fromstring(response.content):
            if child.attrib.get("id") == "168,768,968,868":
                for node in child.findall("currency"):
                    code = node.find("code").text
                    code_to = node.find("codeTo").text

                    if (
                        byn_currency
                        and (code == "USD" and code_to == "BYN")
                        or (code == "BYN" and code_to == "USD")
                    ):
                        create_currency_pair(byn_currency, node)

                    if (
                        eur_currency
                        and (code == "USD" and code_to == "EUR")
                        or (code == "EUR" and code_to == "USD")
                    ):
                        create_currency_pair(eur_currency, node)

                    if (
                        rub_currency
                        and (code == "USD" and code_to == "RUB")
                        or (code == "RUB" and code_to == "USD")
                    ):
                        create_currency_pair(rub_currency, node)

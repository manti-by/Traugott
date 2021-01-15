from rest_framework.generics import ListAPIView

from churchill.api.v1.currency.serializers import CurrencySerializer
from churchill.apps.currencies.models import Currency


class CurrencyView(ListAPIView):

    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()

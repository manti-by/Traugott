from rest_framework import serializers


class CurrencySerializer(serializers.Serializer):

    name = serializers.CharField(max_length=32)
    iso3 = serializers.CharField(max_length=3)
    sign = serializers.CharField(max_length=1, required=False)

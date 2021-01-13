from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from churchill.apps.currencies.models import Currency


class ProfileSerializer(serializers.Serializer):
    image = serializers.ImageField(read_only=True)
    language = serializers.CharField(max_length=5)
    currency = SlugRelatedField(queryset=Currency.objects.all(), slug_field="iso3")
    avg_consumption = serializers.IntegerField()
    avg_price = serializers.DecimalField(max_digits=5, decimal_places=2)

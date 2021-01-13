from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from churchill.apps.currencies.models import Currency


class ProfilesSerializer(serializers.Serializer):
    email = serializers.EmailField()
    image = serializers.ImageField(source="profile.image", read_only=True)
    language = serializers.CharField(source="profile.language", max_length=5)
    currency = SlugRelatedField(source="profile.currency", queryset=Currency.objects.all(), slug_field="iso3")
    avg_consumption = serializers.IntegerField(source="profile.avg_consumption")
    avg_price = serializers.DecimalField(source="profile.avg_price", max_digits=5, decimal_places=2)

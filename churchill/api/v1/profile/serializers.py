from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from churchill.apps.currencies.models import Currency
from churchill.apps.profiles.services import get_profile_stats


class StatsSerializer(serializers.Serializer):
    last_shot_at = serializers.DateTimeField()
    timedelta_last_shot = serializers.DurationField()
    skipped_volume_last_shot = serializers.IntegerField()
    money_saved_last_shot = serializers.DecimalField(max_digits=5, decimal_places=2)


class ProfileSerializer(serializers.Serializer):
    image = serializers.ImageField(read_only=True)
    language = serializers.CharField(max_length=5)
    currency = SlugRelatedField(queryset=Currency.objects.all(), slug_field="iso3")
    avg_consumption = serializers.IntegerField()
    avg_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    stats = serializers.SerializerMethodField()

    def get_stats(self, obj):
        profile_stats = get_profile_stats(obj)
        if profile_stats is not None:
            serializer = StatsSerializer(data=get_profile_stats(obj))
            serializer.is_valid(raise_exception=False)
            return serializer.validated_data

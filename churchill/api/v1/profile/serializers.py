from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from churchill.api.v1.shots.serializers import ShotSerializer
from churchill.apps.core.services import get_timezone_choices
from churchill.apps.currencies.models import Currency
from churchill.apps.profiles.services import get_profile_stats
from churchill.apps.shots.models import Shot


class StatsSerializer(serializers.Serializer):
    last_shot_at = serializers.DateTimeField()
    timedelta_last_shot = serializers.DurationField()
    timedelta_last_shot_repr = serializers.CharField()
    skipped_volume_last_shot = serializers.IntegerField()
    days_to_balance = serializers.IntegerField()
    popular_drink = serializers.CharField(allow_blank=True)
    money_saved_last_shot = serializers.DecimalField(max_digits=5, decimal_places=2)


class ProfileSerializer(serializers.Serializer):
    image = serializers.ImageField(read_only=True)
    language = serializers.CharField(max_length=5)
    currency = SlugRelatedField(queryset=Currency.objects.all(), slug_field="iso3")
    timezone = serializers.ChoiceField(choices=get_timezone_choices())
    avg_consumption = serializers.IntegerField()
    next_day_offset = serializers.IntegerField(required=False)
    avg_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    stats = serializers.SerializerMethodField(read_only=True)
    shots = serializers.SerializerMethodField(read_only=True)

    def get_stats(self, obj):
        profile_stats = get_profile_stats(obj)
        if profile_stats is not None:
            serializer = StatsSerializer(data=profile_stats)
            serializer.is_valid(raise_exception=False)
            return serializer.validated_data

    def get_shots(self, obj):
        shots = Shot.objects.for_user(obj.user)
        return ShotSerializer(shots, many=True).data

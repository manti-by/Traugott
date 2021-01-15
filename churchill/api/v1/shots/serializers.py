from rest_framework import serializers


class ShotSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    volume = serializers.IntegerField()
    degree = serializers.IntegerField(min_value=0, max_value=100)
    cost = serializers.DecimalField(min_value=0, max_digits=5, decimal_places=2)
    created_at = serializers.DateTimeField(read_only=True)

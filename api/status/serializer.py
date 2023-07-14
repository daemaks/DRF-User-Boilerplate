from rest_framework import serializers

from . import services
from user import serializer as user_serialzier


class StatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    date_published = serializers.DateTimeField(read_only=True)
    user = user_serialzier.UserSerialzier(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.StatusDataClass(**data)

from rest_framework import serializers


class DynamicModelSerializer(serializers.Serializer):
    """
    The serializer for creating a dynamic model.
    """

    model_name = serializers.CharField(max_length=255)
    fields = serializers.JSONField()

from rest_framework import serializers
from img_resizer.models import Image


class ImageSerializer(serializers.Serializer):
    image = serializers.CharField(max_length=None, required=True)
    img_hash = serializers.CharField(max_length=32, required=True)

    def create(self, validated_data):
        return Image.objects.create(**validated_data)
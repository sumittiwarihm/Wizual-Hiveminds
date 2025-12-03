from rest_framework import serializers
from .models import IMAGE_STYLES , VIDEO_STYLE_CHOICES

class ImageGenerationSerializer(serializers.Serializer):
    prompt = serializers.CharField()
    style = serializers.ChoiceField(choices=[key for key, _ in IMAGE_STYLES])
class VideoGenerationSerializer(serializers.Serializer):
    prompt=serializers.CharField()
    style = serializers.ChoiceField(choices=[key for key, _ in VIDEO_STYLE_CHOICES ])


from rest_framework import serializers
from .models import VideoSource, Subtitle


class VideoSourceSerializer(serializers.ModelSerializer):
    stream_url = serializers.CharField(read_only=True)

    class Meta:
        model = VideoSource
        fields = ['id', 'quality', 'stream_url', 'is_active']


class SubtitleSerializer(serializers.ModelSerializer):
    file_url = serializers.FileField(source='subtitle_file', read_only=True)

    class Meta:
        model = Subtitle
        fields = ['id', 'language', 'label', 'file_url', 'is_default']

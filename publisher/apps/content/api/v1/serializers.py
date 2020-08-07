from django.urls import reverse
from rest_framework import serializers

from publisher.apps.content.models import (
    Audio,
    Page,
    Text,
    Video
)


class DownloadableSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return obj.url


class PageListSerializer(serializers.ModelSerializer):
    details_url = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = [
            'id',
            'title',
            'details_url',
        ]

    def get_details_url(self, obj):
        return reverse('content_page_v1_detail', kwargs={'pk': obj.pk})


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = [
            'id',
            'title',
            'original_text',
            'counter',
        ]


class AudioSerializer(DownloadableSerializer):
    class Meta:
        model = Audio
        fields = [
            'id',
            'title',
            'bitrate',
            'url',
            'counter',
        ]


class VideoSerializer(DownloadableSerializer):
    subtitles = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id',
            'title',
            'subtitles',
            'url',
            'counter',
        ]

    def get_subtitles(self, obj):
        return obj.subtitles


class PageSerializer(serializers.ModelSerializer):
    texts = TextSerializer(many=True)
    audios = AudioSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        model = Page
        fields = '__all__'

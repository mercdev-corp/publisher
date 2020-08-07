from django.contrib import admin

from .models import (
    Audio,
    Page,
    Text,
    Video
)


class TextInline(admin.StackedInline):
    model = Text
    extra = 1


class AudioInline(admin.StackedInline):
    model = Audio
    extra = 1


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


class TextAdmin(admin.ModelAdmin):
    model = Text


class AudioAdmin(admin.ModelAdmin):
    model = Audio


class VideoAdmin(admin.ModelAdmin):
    model = Video


class PageAdmin(admin.ModelAdmin):
    inlines = [
        TextInline,
        AudioInline,
        VideoInline,
    ]


admin.site.register(Page, PageAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Video, VideoAdmin)

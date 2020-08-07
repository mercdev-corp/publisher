from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Countable(models.Model):
    counter = models.IntegerField(verbose_name=_('counter'), blank=True, default=0)

    class Meta:
        abstract = True


class Entitled(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=1024, blank=True, default='')

    class Meta:
        abstract = True
        ordering = ['pk']


class Page(Entitled):
    pass


class Content(Countable, Entitled):
    page = models.ForeignKey(verbose_name=_('page'), to=Page, on_delete=models.SET_NULL,
                             null=True, related_name="%(class)ss",
                             related_query_name="%(class)ss",)
    order = models.IntegerField(verbose_name=_('order'), blank=True, default=0)

    class Meta:
        abstract = True
        ordering = ['order', 'pk']


def uploadable_content_path(instance, filename):
    return default_storage.get_available_name(
        Path('content', str(instance.page_id), instance.__class__.__name__, filename))


class DownloadableContent(Content):
    local = models.FileField(verbose_name=_('local file'), upload_to=uploadable_content_path,
                             null=True, blank=True,)
    remote = models.URLField(verbose_name=_('remote URL'), null=True, blank=True)

    class Meta(Content.Meta):
        abstract = True

    @property
    def url(self):
        return self.remote or self.local.url

    def clean(self):
        super().clean()

        if not self.remote and not self.local:
            raise ValidationError({
                'local': _('Either `local file` or `remote URL` field should be set'),
                'remote': _('Either `local file` or `remote URL` field should be set'),
            })


class Audio(DownloadableContent):
    bitrate = models.IntegerField(verbose_name=_('bitrate'))


class Text(Content):
    original_text = models.TextField(verbose_name=_('original text'))


class Video(DownloadableContent):
    local_subtitles = models.FileField(verbose_name=_('local subtitles'), null=True, blank=True,
                                       upload_to=uploadable_content_path)
    remote_subtitles = models.URLField(verbose_name=_('subtitles URL'), null=True, blank=True)

    @property
    def subtitles(self):
        if not self.remote_subtitles and not self.local_subtitles:
            return ''

        return self.remote_subtitles or self.local_subtitles.url

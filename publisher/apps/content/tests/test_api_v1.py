from django.urls import reverse
from django_webtest import TransactionWebTest
from model_bakery import baker

from publisher.apps.content.models import (
    Audio,
    Page,
    Text,
    Video
)


class ContentTest(TransactionWebTest):
    def setUp(self):
        self.page0 = baker.make(Page, title='Page 0')
        self.page1 = baker.make(Page, title='Page 1')
        self.page2 = baker.make(Page, title='Page 2')

        # page0
        self.video0 = baker.make(Video, title='Video 0', order=7, page=self.page0,
                                 remote='http://example.com/video0.mp4',
                                 remote_subtitles='http://example.com/video0.srt')
        self.video1 = baker.make(Video, title='Video 1', order=3, page=self.page0,
                                 remote='http://example.com/video1.mp4')
        self.video2 = baker.make(Video, title='Video 2', order=3, page=self.page0,
                                 remote='http://example.com/video2.mp4')

        self.audio0 = baker.make(Audio, title='Audio 0', order=1, page=self.page0, bitrate=128,
                                 remote='http://example.com/audeo0.mp3')
        self.audio1 = baker.make(Audio, title='Audio 1', order=0, page=self.page0, bitrate=320,
                                 remote='http://example.com/audeo0.mp3')

        self.text0 = baker.make(Text, title='Text 0', order=7, page=self.page0)
        self.text1 = baker.make(Text, title='Text 1', order=7, page=self.page0)
        self.text2 = baker.make(Text, title='Text 2', order=2, page=self.page0,
                                original_text='Text 2 content')
        self.text3 = baker.make(Text, title='Text 3', order=7, page=self.page0)

        # page1
        self.video3 = baker.make(Video, title='Video 3', page=self.page1,
                                 remote='http://example.com/video3.mp4')
        self.text4 = baker.make(Text, title='Text 4', page=self.page1,
                                original_text='Text 4 content')

        # page2
        self.text5 = baker.make(Text, title='Text 5', page=self.page2)
        self.audio2 = baker.make(Audio, title='Audio 2', page=self.page2,
                                 remote='http://example.com/audeo2.mp3')

    def page_url(self, page):
        return reverse('content_page_v1_detail', kwargs={'pk': page.pk})

    def test_content_list(self):
        url = reverse('content_page_v1_list')

        # test main list
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, resp.json['count'])
        self.assertEqual(1, len(resp.json['results']))
        self.assertTrue(resp.json['next'])
        self.assertFalse(resp.json['previous'])
        self.assertEqual(self.page0.pk, resp.json['results'][0]['id'])
        self.assertEqual(self.page0.title, resp.json['results'][0]['title'])

        # test second page
        resp = self.app.get(resp.json['next'])
        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, resp.json['count'])
        self.assertEqual(1, len(resp.json['results']))
        self.assertTrue(resp.json['next'])
        self.assertTrue(resp.json['previous'])
        self.assertEqual({
            'id': self.page1.pk,
            'title': self.page1.title,
            'details_url': self.page_url(self.page1),
        }, resp.json['results'][0])

    def test_content_details(self):
        url = self.page_url(self.page0)

        self.assertEqual(0, Video.objects.get(pk=self.video1.pk).counter)

        # test page
        resp = self.app.get(url)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(3, len(resp.json['videos']))
        self.assertEqual(2, len(resp.json['audios']))
        self.assertEqual(4, len(resp.json['texts']))

        # check content
        self.assertEqual({
            'id': self.video1.pk,
            'title': self.video1.title,
            'url': self.video1.remote,
            'subtitles': '',
            'counter': 0,
        }, resp.json['videos'][0])
        self.assertEqual({
            'id': self.video0.pk,
            'title': self.video0.title,
            'url': self.video0.remote,
            'subtitles': self.video0.remote_subtitles,
            'counter': 0,
        }, resp.json['videos'][2])

        self.assertEqual({
            'id': self.audio0.pk,
            'title': self.audio0.title,
            'url': self.audio0.remote,
            'bitrate': self.audio0.bitrate,
            'counter': 0,
        }, resp.json['audios'][1])

        self.assertEqual({
            'id': self.text2.pk,
            'title': self.text2.title,
            'original_text': self.text2.original_text,
            'counter': 0,
        }, resp.json['texts'][0])
        self.assertEqual({
            'id': self.text0.pk,
            'title': self.text0.title,
            'original_text': self.text0.original_text,
            'counter': 0,
        }, resp.json['texts'][1])

        # check counter
        self.assertEqual(1, Video.objects.get(pk=self.video1.pk).counter)
        self.assertEqual(0, Audio.objects.get(pk=self.audio2.pk).counter)

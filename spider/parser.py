# coding: utf-8
from spider.models import Process


def parser_artist(artist_id):
    process = Process.objects.get_or_create(pk=artist_id)
    if process.is_success:
        return

    print('Starting fetch artist:{}'.format(artist_id))



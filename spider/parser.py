# coding: utf-8
from spider.models import Process


def parser_artist(artist_id):
    process,is_created = Process.objects.get_or_create(pk=artist_id)
    if not is_created:
        return

    print('Starting fetch artist:{}'.format(artist_id))




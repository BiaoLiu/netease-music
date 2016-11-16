# coding: utf-8
import time

from spider.models import Process, Artist, Song, NeteaseUser, Comment
from spider.utils import get_html, post

DISCOVER_URL = 'http://music.163.com/discover/artist/cat?id={}&initial={}'
ARTIST_URL = 'http://music.163.com/artist?id={}'
SONG_URL = 'http://music.163.com/song?id={}'
COMMENTS_URL = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}'  # noqa


def parser_artist_list(cat_id, initial_id):
    tree = get_html(DISCOVER_URL.format(cat_id, initial_id))
    artist_items = tree.xpath('//a[contains(@class, "nm-icn")]/@href')

    return [item.split('=')[1] for item in artist_items]


def unprocess_artist_list():
    """
    等待处理的歌手列表
    :return:
    """
    unprocess = Process.objects.filter(status=0)
    return [p.id for p in unprocess]


def parser_artist(artist_id):
    '''
    抓取歌手信息
    :param artist_id:
    :return:
    '''
    process, is_created = Process.objects.get_or_create(pk=artist_id)
    # if not is_created:
    #     return

    print('Starting fetch artist: {}'.format(artist_id))
    start = time.time()

    tree = get_html(ARTIST_URL.format(artist_id))

    artists = Artist.objects.filter(id=artist_id)
    if not artists:
        artist_name = tree.xpath('//h2[@id="artist-name"]/text()')[0]
        picture = tree.xpath(
            '//div[contains(@class, "n-artist")]//img/@src')[0]

        artist = Artist(id=artist_id, name=artist_name, picture=picture)
        artist.save()
    else:
        artist = artists[0]

    # 歌手热门50首歌曲
    song_items = tree.xpath('//div[@id="artist-top50"]//ul/li/a/@href')
    # songs = []
    for item in song_items:
        song_id = item.split('=')[1]
        song = parser_song(song_id, artist)
        # if song is not None:
        #     songs.append(song)

    process.make_succeed()

    print('Finished fetch artist: {} Cost: {}'.format(
        artist_id, time.time() - start))


def parser_song(song_id, artist):
    """
    抓取歌手热门50首歌曲以及歌曲热门评论
    :param song_id:
    :param artist:
    :return:
    """
    tree = get_html(SONG_URL.format(song_id))
    song = Song.objects.filter(id=song_id)

    r = post(COMMENTS_URL.format(song_id))
    if r.status_code != 200:
        print('API Error: Song {}'.format(song_id))
        return

    data = r.json()
    if not song:
        for404 = tree.xpath('//div[@class="n-for404"]')
        if for404:
            return

        try:
            song_name = tree.xpath('//em[@class="f-ff2"]/text()')[0].strip()
        except IndexError:
            try:
                song_name = tree.xpath(
                    '//meta[@name="keywords"]/@content')[0].strip()
            except IndexError:
                print('Fetch limit!')
                time.sleep(10)
                return parser_song(song_id, artist)
        # 保存歌手歌曲
        song = Song(id=song_id, name=song_name, artist=artist, comment_count=data['total'])
        song.save()
    else:
        song = song[0]
        for comment_ in data['hotComments']:
            comment_id = comment_['commentId']
            content = comment_['content']
            like_count = comment_['likedCount']
            user = comment_['user']
            if not user:
                continue

            netease_user = NeteaseUser.objects.filter(id=user['userId'])
            if not netease_user:
                netease_user = NeteaseUser(name=user['nickname'], picture=user['avatarUrl'])
                netease_user.save()

            try:
                comment = Comment.objects.get(id=comment_id)
            except Comment.DoesNotExist:
                # 保存歌曲评论
                comment = Comment(content=content, like_count=like_count, user=user, song=song)
                comment.save()

        time.sleep(1)
        return song

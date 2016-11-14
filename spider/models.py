from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

ARTIST_URL = 'http://music.163.com/#/artist?id={}'
SONG_URL = 'http://music.163.com/#/song?id={}'
USER_URL = 'http://music.163.com/#/user/home?id={}'
SAMPLE_SIZE = 200
TOTAL_SIZE = 2000

RANDOM_KEY = 'commentbox:random:{session_id}'
STAR_KEY = 'commentbox:star'
OBJ_KEY = 'commentbox:object:{coll_name}:{id}'
SEARCH_KEY = 'commentbox:search:{type}:{id}'
SUGGEST_KEY = 'commentbox:suggest:{text}'
TIMEOUT = 60 * 60


class BaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthUser(AbstractUser):
    picture = models.CharField(max_length=200, null=True)

    @property
    def url(self):
        return USER_URL.format(self.id)


class NeteaseUser(BaseModel):
    name = models.CharField(max_length=100, null=True)
    picture = models.CharField(max_length=200, null=True)


class Artist(BaseModel):
    name = models.CharField(max_length=100, null=True)
    picture = models.CharField(max_length=200, null=True)

    # songs = db.ListField(db.ReferenceField('Song'))

    class Meta(BaseModel.Meta):
        index_together = ['name']

    @property
    def url(self):
        return ARTIST_URL.format(self.id)


class Song(BaseModel):
    name = models.CharField(max_length=100, null=True)
    comment_count = models.IntegerField()

    # comments = db.ListField(db.ReferenceField('Comment'))
    artist = models.ForeignKey(Artist)

    class Meta(BaseModel.Meta):
        index_together = ['name']

    @property
    def url(self):
        return SONG_URL.format(self.id)

    @property
    def artist_url(self):
        return self.artist.url


class Comment(BaseModel):
    content = models.CharField(max_length=100, null=True)
    like_count = models.IntegerField()
    user = models.ForeignKey(AuthUser)
    song = models.ForeignKey(Song)

    # meta = {
    #     'indexes': [
    #         '-like_count'
    #     ]
    # }

    @property
    def user_url(self):
        return self.user.url

    @property
    def user_url(self):
        return self.song.artist_url

        artist = {
            'id': artist_obj.id,
            'avatar': artist_obj.picture,
            'name': artist_obj.name,
            'url': artist_obj.url
        }

        user = {
            'avatar': user_obj.picture,
            'name': user_obj.name,
            'url': user_obj.url
        }
        return {
            'song': song,
            'user': user,
            'artist': artist,
            'content': self.content
        }


PROCESS_STATUS = (
    ('PENDING', 0),
    ('SUCCEEDED', 1),
    ('FAILED', 2)
)


class Process(BaseModel):
    status = models.IntegerField(choices=PROCESS_STATUS, default=0)

    @property
    def is_success(self):
        return self.status == 1

    def make_succeed(self):
        return self.objects.update(status=1)

    def make_fail(self):
        return self.objects.update(status=2)

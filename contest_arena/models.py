from uuid import uuid4
from django.db import models


def get_meme_image_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'meme_images/{0}'.format(filename)


def get_meme_sound_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'meme_sounds/{0}'.format(filename)


class Meme(models.Model):
    image = models.ImageField(upload_to=get_meme_image_upload_path)
    sound = models.FileField(upload_to=get_meme_sound_upload_path)
    text = models.TextField()
    meme_for = models.IntegerField(default=-1, help_text="Alum = 0 & Student = 1")
    meme_type = models.IntegerField(default=-1, help_text="Fail = 0 & Success = 1")

    def __str__(self):
        return self.text

    class META:
        verbose_name_plural = "Memes"

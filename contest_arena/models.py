from uuid import uuid4
from django.db import models
from django.utils.safestring import mark_safe


# ------------------------------------------------------------>>> Media Files Upload path start <<<--------------------
def get_meme_image_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/meme_images/<filename>
    # file named by UUID
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'meme_images/{0}'.format(filename)


def get_meme_sound_upload_path(instance, name):
    # file will be uploaded to MEDIA_ROOT/meme_sounds/<filename>
    # file named by UUID
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'meme_sounds/{0}'.format(filename)


def get_puzzle_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/puzzles/<filename>
    # file named by UUID
    print(instance.id)
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'puzzles/{0}'.format(filename)


# ------------------------------------------------------------>>> Media Files Upload path end <<<----------------------


# --------------------------------------------------------------------------->>> Models start <<<----------------------

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


class Puzzle(models.Model):
    id = models.IntegerField(primary_key=True)
    info = models.CharField(null=True, blank=True, max_length=300)
    info_link = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to=get_puzzle_upload_path, null=True)
    ans = models.CharField(null=False, max_length=200)
    visible = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Puzzle"

    def __str__(self):
        return self.ans

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def img_show(self):  # receives the instance as an argument
        return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
            thumb=self.image.url,
        ))

    img_show.allow_tags = True
    img_show.short_description = 'Current Puzzle'

# ----------------------------------------------------------------------------->>> Models end <<<----------------------

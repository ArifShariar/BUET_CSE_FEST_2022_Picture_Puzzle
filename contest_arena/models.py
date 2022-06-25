from uuid import uuid4
from django.db import models
from django.utils.safestring import mark_safe
from user.models import Participant


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


def get_hackerman_image_upload_path(instance, name):
    ext = name.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'hackerman/{0}'.format(filename)


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

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def get_sound(self):
        if self.sound and hasattr(self.sound, 'url'):
            return self.sound.url
        return None

    class META:
        verbose_name_plural = "Memes"


class Puzzle(models.Model):
    level = models.IntegerField(null=True)
    info = models.CharField(null=True, blank=True, max_length=300)
    info_link = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(upload_to=get_puzzle_upload_path, null=True)
    ans = models.CharField(null=False, max_length=50)
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


class HackerManImage(models.Model):
    image = models.ImageField(upload_to=get_hackerman_image_upload_path)
    image_for = models.IntegerField(default=-1, help_text="Alum = 0 & Student = 1")

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def img_show(self):  # receives the instance as an argument
        return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
            thumb=self.image.url,
        ))

    img_show.allow_tags = True
    img_show.short_description = 'Current Hackerman Image'

    class META:
        verbose_name_plural = "Hackerman Images"


class AlumniHackermanQuote(models.Model):
    message = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.message

    class META:
        verbose_name_plural = "Alumni Hackerman Quote"


class CurrentStudentHackerQuote(models.Model):
    message = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.message

    class META:
        verbose_name_plural = "Current Student Hackerman Quote"


# ----------------------------------------------------------------------------->>> Models end <<<----------------------

class PuzzleForm(models.Model):
    participant = models.OneToOneField(Participant, on_delete=models.CASCADE)
    puzzle = models.OneToOneField(Puzzle, on_delete=models.CASCADE)
    ans = models.TextField()

    class META:
        verbose_name_plural = "PuzzleForm"

    def __str__(self):
        return self.puzzle.title + " - " + self.participant.user.username + " - " + self.ans

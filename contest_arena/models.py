from django.db import models


# Create your models here.

def get_meme_image_upload_path(instance, name):
    print(instance.meme_id)
    return 'meme_images/{0}/{1}'.format(instance.meme_id, name)


def get_meme_sound_upload_path(instance, name):
    return 'meme_sounds/{0}/{1}'.format(instance.meme_id, name)


class Meme(models.Model):
    # # add an image field
    meme_id = models.AutoField(unique=True)
    image = models.ImageField(upload_to=get_meme_image_upload_path)
    sound = models.FileField(upload_to=get_meme_sound_upload_path)
    text = models.TextField()
    meme_for = models.IntegerField(default=-1, help_text="Alum = 0 & Student = 1")
    meme_type = models.IntegerField(default=-1, help_text="Fail = 0 & Success = 1")

    def __str__(self):
        return self.text

    class META:
        verbose_name_plural = "Memes"

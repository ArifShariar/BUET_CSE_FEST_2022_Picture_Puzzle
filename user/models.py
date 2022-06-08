from django.db import models
from django.contrib.auth.models import User


# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_type = models.IntegerField(default=0)  # Alum -> 1, Current student -> 2
    batch = models.IntegerField(default=0)
    student_ID = models.IntegerField(default=0)
    curr_level = models.IntegerField(default=0)
    position = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_participant'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):

    if created:
        Participant.objects.create(user=instance)

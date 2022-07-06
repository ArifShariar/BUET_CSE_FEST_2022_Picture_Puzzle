from django.contrib.auth.models import User
from django.db import models

from CSE_FEST_2022_Picture_Puzzle import settings


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_type = models.IntegerField(default=0, help_text="Alum = 1 & Student = 2")
    student_ID = models.CharField(max_length=7, unique=True)
    batch = models.IntegerField(default=0)
    curr_level = models.IntegerField(default=1)
    last_successful_submission_time = models.DateTimeField(default=None, blank=True, null=True)
    max_weight = models.FloatField(default=settings.START_PROB)
    # this field will be used by the admin to temporarily activate or deactivate a participant
    disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_participant'

# required for creating a participant profile for superuser
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Participant.objects.create(user=instance)

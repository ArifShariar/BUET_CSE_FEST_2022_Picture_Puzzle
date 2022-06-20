from django.contrib.auth.models import User
from django.db import models


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_type = models.IntegerField(default=0, help_text="Alum = 1 & Student = 2")
    batch = models.IntegerField(default=0)
    student_ID = models.IntegerField(default=0)
    curr_level = models.IntegerField(default=0)
    position = models.IntegerField(default=0)
    # this field will be used by the admin to temporarily activate or deactivate a participant
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_participant'

# required for creating a participant profile for superuser
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Participant.objects.create(user=instance)

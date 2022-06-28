from user.models import Participant
from django.db import models


# Create your models here.


class Submission(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    time = models.DateTimeField(null=False)
    status = models.IntegerField(default=0, help_text="Incorrect = 0 & Correct = 1")
    ans = models.CharField(null=False, max_length=50)


class DetectorGraph(models.Model):
    participant1 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant1')
    participant2 = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='participant2')
    weight = models.FloatField(default=0.5)

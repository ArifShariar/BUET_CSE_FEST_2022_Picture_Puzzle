from django.contrib import admin
from .models import *


# Register your models here.

class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'acc_type', 'student_ID', 'curr_level', 'last_successful_submission_time', 'disabled')


admin.site.register(Participant, ParticipantAdmin)

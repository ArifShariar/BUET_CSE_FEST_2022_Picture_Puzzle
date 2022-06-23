from django.contrib import admin
from .models import *


# Register your models here.
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('participant', 'level', 'time', 'status', 'ans')


admin.site.register(Submission, SubmissionAdmin)

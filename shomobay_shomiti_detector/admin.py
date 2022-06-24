from django.contrib import admin
from .models import *


# Register your models here.
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('participant', 'level', 'time', 'status', 'ans')


class DetectorGraphAdmin(admin.ModelAdmin):
    list_display = ('participant1', 'participant2', 'weight')


admin.site.register(Submission, SubmissionAdmin)
admin.site.register(DetectorGraph, DetectorGraphAdmin)

from django.contrib import admin
from .models import *


# Register your models here.
class MemeAdmin(admin.ModelAdmin):
    list_display = ('text', 'meme_for', 'meme_type', 'test_link')


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('level', 'title', 'ans', 'visible', 'info', 'image', 'info_link')


class HackerManImageAdmin(admin.ModelAdmin):
    list_display = ('image_for', 'image', 'test_link')


class AlumniHackermanQuoteAdmin(admin.ModelAdmin):
    list_display = ('message',)


class CurrentStudentHackerQuoteAdmin(admin.ModelAdmin):
    list_display = ('message',)


admin.site.register(Meme, MemeAdmin)
admin.site.register(Puzzle, PuzzleAdmin)
admin.site.register(HackerManImage, HackerManImageAdmin)
admin.site.register(AlumniHackermanQuote, AlumniHackermanQuoteAdmin)
admin.site.register(CurrentStudentHackerQuote, CurrentStudentHackerQuoteAdmin)

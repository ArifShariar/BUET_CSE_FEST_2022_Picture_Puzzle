# Generated by Django 4.0.5 on 2022-06-28 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest_arena', '0011_alter_hackermanimage_image_for_alter_meme_meme_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hackermanimage',
            name='image_for',
            field=models.IntegerField(default=0, help_text='All = 0, Alum = 1, Student = 2'),
        ),
        migrations.AlterField(
            model_name='meme',
            name='meme_for',
            field=models.IntegerField(default=0, help_text='All = 0, Alum = 1, Student = 2'),
        ),
    ]

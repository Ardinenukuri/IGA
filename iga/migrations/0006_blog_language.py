# Generated by Django 4.2.6 on 2023-11-13 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iga', '0005_remove_blog_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('ki', 'kirundi')], default='en', max_length=10),
            preserve_default=False,
        ),
    ]

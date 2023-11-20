"""
leave\migrations\0001_initial.py - Initial migration for the 'leave' app.

This module defines the initial database schema for the 'leave' app.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Database migration to create the initial schema for the 'leave' app.
    """

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField()),
            ],
        ),
    ]

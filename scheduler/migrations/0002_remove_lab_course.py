# Generated by Django 5.1.3 on 2024-12-19 01:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lab',
            name='course',
        ),
    ]

# Generated by Django 5.0 on 2024-01-21 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ottapp', '0016_delete_sub'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='email',
        ),
    ]

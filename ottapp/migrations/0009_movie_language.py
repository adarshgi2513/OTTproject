# Generated by Django 5.0 on 2024-01-13 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ottapp', '0008_alter_subscription_subscription_plan_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.CharField(default='', max_length=55),
        ),
    ]

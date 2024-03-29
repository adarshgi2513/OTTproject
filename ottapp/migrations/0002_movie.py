# Generated by Django 5.0 on 2024-01-02 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ottapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('release_date', models.DateField()),
                ('thumbnail', models.ImageField(upload_to='thumbnails/')),
                ('video', models.FileField(upload_to='videos/')),
            ],
        ),
    ]

# Generated by Django 2.0.2 on 2018-02-18 20:11

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tea',
            name='image',
            field=models.ImageField(default='default.png', upload_to=core.models.tea_image_upload),
            preserve_default=False,
        ),
    ]
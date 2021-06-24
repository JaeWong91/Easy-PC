# Generated by Django 3.2.4 on 2021-06-24 14:19

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_url',
            field=models.URLField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='snippet',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
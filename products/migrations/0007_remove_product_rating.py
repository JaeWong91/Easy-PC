# Generated by Django 3.2.4 on 2021-06-22 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_productreview_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]

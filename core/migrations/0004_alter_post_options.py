# Generated by Django 3.2.2 on 2021-05-09 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_post_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['post_datetime']},
        ),
    ]
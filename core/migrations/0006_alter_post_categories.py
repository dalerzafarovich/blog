# Generated by Django 3.2.2 on 2021-05-09 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210509_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='posts', to='core.Category'),
        ),
    ]

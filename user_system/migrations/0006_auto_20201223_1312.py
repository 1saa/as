# Generated by Django 3.1.4 on 2020-12-23 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0005_auto_20201223_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='last_time',
            field=models.DateTimeField(null=True),
        ),
    ]
# Generated by Django 3.1.4 on 2020-12-21 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0003_auto_20201222_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='papers',
            name='file',
            field=models.URLField(default='file\\0.pdf'),
        ),
    ]

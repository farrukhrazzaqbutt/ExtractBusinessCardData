# Generated by Django 3.0.5 on 2020-05-07 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_scanner', '0004_auto_20200506_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scancard',
            name='description',
            field=models.TextField(default=''),
        ),
    ]

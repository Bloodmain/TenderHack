# Generated by Django 4.1.7 on 2023-04-01 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0006_okpd'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='category',
            field=models.CharField(default='', max_length=400, null=True, verbose_name='Категории'),
        ),
    ]

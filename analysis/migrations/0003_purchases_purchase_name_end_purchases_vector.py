# Generated by Django 4.1.7 on 2023-04-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_alter_purchases_contract_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='purchase_name_end',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='purchases',
            name='vector',
            field=models.BinaryField(default=b''),
        ),
    ]
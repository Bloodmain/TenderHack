# Generated by Django 4.1.7 on 2023-04-01 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0010_alter_contracts_contract_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participants',
            name='part_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part', to='analysis.purchases', verbose_name='Номер закупки'),
        ),
    ]

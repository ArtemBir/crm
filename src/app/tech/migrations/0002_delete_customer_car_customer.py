# Generated by Django 5.1.4 on 2025-01-29 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('customers', '0001_initial'),
        ('tech', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.AddField(
            model_name='car',
            name='customer',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='cars',
                to='customers.customer',
            ),
        ),
    ]

# Generated by Django 3.1.2 on 2021-01-17 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Download', '0009_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(max_length=200),
        ),
    ]
# Generated by Django 3.1.2 on 2021-01-17 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Download', '0008_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='status',
            field=models.CharField(default='Failed', max_length=200),
        ),
    ]

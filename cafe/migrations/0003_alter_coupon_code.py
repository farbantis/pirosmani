# Generated by Django 4.0.6 on 2023-05-20 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]

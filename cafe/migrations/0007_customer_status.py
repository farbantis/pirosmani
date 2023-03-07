# Generated by Django 4.0.4 on 2022-06-04 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_customer_order_orderitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('Golden', 'Золотой'), ('Silver', 'Серебрянный'), ('Bronze', 'Бронзовый')], default='Bronze', max_length=10),
        ),
    ]

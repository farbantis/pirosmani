# Generated by Django 4.0.4 on 2022-05-12 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_alter_menu_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture_ext',
            field=models.ImageField(blank=True, null=True, upload_to='products/'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='ww'),
        ),
    ]
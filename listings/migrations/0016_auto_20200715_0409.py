# Generated by Django 3.0.3 on 2020-07-15 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0015_auto_20200715_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(blank=True, help_text='Select all images at once', null=True, upload_to='listings_upld/gallery'),
        ),
    ]
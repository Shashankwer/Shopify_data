# Generated by Django 3.1.2 on 2020-10-25 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_app_dev', '0006_auto_20201025_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abandoncartlineitem',
            name='variant_title',
        ),
    ]
# Generated by Django 3.1.2 on 2020-10-25 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopify_app_dev', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='option_1',
        ),
        migrations.RemoveField(
            model_name='product',
            name='option_2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='option_3',
        ),
        migrations.CreateModel(
            name='ProductOptions',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=200)),
                ('position', models.IntegerField(default=1)),
                ('values', models.CharField(default='', max_length=1000)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopify_app_dev.product')),
            ],
        ),
    ]

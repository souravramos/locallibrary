# Generated by Django 3.0.8 on 2020-08-04 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20200804_1453'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='first_name_sourav',
            new_name='first_name',
        ),
    ]

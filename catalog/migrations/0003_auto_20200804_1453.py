# Generated by Django 3.0.8 on 2020-08-04 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='first_name',
            new_name='first_name_sourav',
        ),
    ]

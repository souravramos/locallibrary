# Generated by Django 3.0.8 on 2020-08-06 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_book_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.CharField(max_length=5, null=True, verbose_name='Price'),
        ),
    ]

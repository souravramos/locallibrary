# Generated by Django 3.0.8 on 2020-08-06 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_book_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='image',
        ),
        migrations.AlterField(
            model_name='book',
            name='buy_online',
            field=models.CharField(blank=True, help_text='Enter a link to buy this book online', max_length=200, null=True, verbose_name='Buy Online'),
        ),
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Edition'),
        ),
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='Price(INR)'),
        ),
    ]

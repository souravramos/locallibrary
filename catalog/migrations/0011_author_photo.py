# Generated by Django 3.0.8 on 2020-08-10 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_auto_20200806_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='photo',
            field=models.ImageField(default='default.jpg', upload_to='catalog/static/catalog/images'),
        ),
    ]
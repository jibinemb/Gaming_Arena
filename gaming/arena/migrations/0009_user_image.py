# Generated by Django 2.2.7 on 2023-05-26 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0008_auto_20230526_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='nothing', upload_to='user'),
        ),
    ]
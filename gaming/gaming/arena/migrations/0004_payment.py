# Generated by Django 4.1.7 on 2023-05-25 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arena', '0003_booking_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=25)),
                ('amount', models.IntegerField()),
                ('cardno', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('bookid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arena.booking')),
            ],
        ),
    ]
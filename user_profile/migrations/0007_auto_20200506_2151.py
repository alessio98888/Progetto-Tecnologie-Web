# Generated by Django 3.0.5 on 2020-05-06 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20200506_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='certifiedFrom',
            field=models.CharField(max_length=75, verbose_name='Certified From'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='name',
            field=models.CharField(max_length=75),
        ),
    ]
# Generated by Django 3.0.5 on 2020-05-04 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_auto_20200504_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='birth_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]

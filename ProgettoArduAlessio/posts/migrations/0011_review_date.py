# Generated by Django 3.0.5 on 2020-05-10 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20200510_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]

# Generated by Django 3.0.5 on 2020-05-08 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_offer_deleted_but_visible_home'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='deleted_but_visible_home',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]

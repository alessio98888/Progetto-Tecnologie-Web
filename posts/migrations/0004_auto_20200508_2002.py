# Generated by Django 3.0.5 on 2020-05-08 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='posts.Currency'),
        ),
        migrations.AddField(
            model_name='request',
            name='currency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='posts.Currency'),
        ),
    ]

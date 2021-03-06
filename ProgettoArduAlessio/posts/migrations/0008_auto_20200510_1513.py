# Generated by Django 3.0.5 on 2020-05-10 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20200510_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='offers', to='posts.Category'),
        ),
        migrations.AddField(
            model_name='request',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='requests', to='posts.Category'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-05-05 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='language',
            name='language_level',
        ),
        migrations.CreateModel(
            name='LanguageProficiency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='levels', to='user_profile.LanguageLevel')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='languages', to='user_profile.Language')),
            ],
        ),
    ]

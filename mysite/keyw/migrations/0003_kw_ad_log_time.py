# Generated by Django 2.0.7 on 2018-11-14 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyw', '0002_kw_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='kw_ad',
            name='log_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

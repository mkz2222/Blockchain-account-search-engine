# Generated by Django 2.0.7 on 2018-11-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keyw', '0004_auto_20181114_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='kw_ad',
            name='filename_m',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

# Generated by Django 2.0.7 on 2018-12-01 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acct', '0007_auto_20181201_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acct_info',
            name='dapp',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]

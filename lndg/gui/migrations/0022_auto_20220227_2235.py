# Generated by Django 3.2.7 on 2022-02-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0021_auto_20220221_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='failedhtlcs',
            name='chan_out_liq',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='failedhtlcs',
            name='chan_out_pending',
            field=models.BigIntegerField(null=True),
        ),
    ]

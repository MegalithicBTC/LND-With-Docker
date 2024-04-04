# Generated by Django 3.2.7 on 2021-09-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0002_auto_20210923_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channels',
            old_name='base_fee',
            new_name='local_base_fee',
        ),
        migrations.RenameField(
            model_name='channels',
            old_name='fee_rate',
            new_name='local_fee_rate',
        ),
        migrations.AddField(
            model_name='channels',
            name='remote_base_fee',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='channels',
            name='remote_fee_rate',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

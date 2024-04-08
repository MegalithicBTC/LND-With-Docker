# Generated by Django 3.2.7 on 2021-10-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gui', '0010_rebalancer_payment_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingHTLCs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incoming', models.BooleanField()),
                ('amount', models.BigIntegerField()),
                ('hash_lock', models.CharField(max_length=64)),
                ('expiration_height', models.IntegerField()),
                ('forwarding_channel', models.IntegerField()),
                ('alias', models.CharField(max_length=32)),
            ],
        ),
    ]
# Generated by Django 3.2.9 on 2021-11-10 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade_simulation', '0003_auto_20211110_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14, null=True),
        ),
    ]

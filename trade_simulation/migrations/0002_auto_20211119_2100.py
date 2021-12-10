# Generated by Django 3.2.9 on 2021-11-20 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade_simulation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['created_on']},
        ),
        migrations.AlterField(
            model_name='holding',
            name='ticker',
            field=models.TextField(max_length=5),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='game_rank',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='portfolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='trade_simulation.portfolio'),
        ),
    ]

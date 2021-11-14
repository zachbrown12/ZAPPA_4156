# Generated by Django 3.2.9 on 2021-11-14 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("trade_simulation", "0004_auto_20211114_0555")]

    operations = [
        migrations.RenameField(
            model_name="game", old_name="startingBalance", new_name="starting_balance"
        ),
        migrations.RenameField(model_name="game", old_name="id", new_name="uid"),
        migrations.RenameField(model_name="holding", old_name="id", new_name="uid"),
        migrations.RenameField(model_name="portfolio", old_name="id", new_name="uid"),
        migrations.RenameField(
            model_name="transaction", old_name="tradeType", new_name="trade_type"
        ),
        migrations.RenameField(model_name="transaction", old_name="id", new_name="uid"),
    ]

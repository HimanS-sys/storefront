# Generated by Django 5.0.4 on 2024-04-28 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_address_zip_customer_store_custo_lastnam_bcd537_idx"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product", old_name="price", new_name="unit_price",
        ),
    ]
# Generated by Django 4.2.1 on 2023-06-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_zip_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="email",
            field=models.EmailField(max_length=70),
        ),
    ]
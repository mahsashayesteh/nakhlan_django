# Generated by Django 4.2.1 on 2023-06-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_variation"),
        ("carts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="variation",
            field=models.ManyToManyField(blank=True, to="store.variation"),
        ),
    ]

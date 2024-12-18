# Generated by Django 4.2.3 on 2023-08-06 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0017_brandsname_is_available_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="slider",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="photos/slider_imgs")),
                (
                    "discount_deal",
                    models.CharField(
                        choices=[
                            ("پیشنهاد ویژه", "پیشنهاد ویژه"),
                            ("جدیدترین ها", "جدیدترین ها"),
                        ],
                        max_length=100,
                    ),
                ),
                ("sale", models.IntegerField()),
                ("discount", models.IntegerField()),
                ("brand_name", models.CharField(max_length=200)),
                ("like", models.CharField(max_length=200)),
            ],
        ),
    ]

# Generated by Django 4.2.3 on 2023-09-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0011_blogdetails_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogdetails",
            name="subject",
            field=models.CharField(
                db_collation="utf8_persian_ci", max_length=225, unique=True
            ),
        ),
    ]

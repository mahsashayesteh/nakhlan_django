# Generated by Django 4.2.3 on 2023-09-07 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0021_alter_section_name_filter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="section",
            name="name_filter",
            field=models.CharField(
                default="null", max_length=100, verbose_name="نام برای فیلتر کردن"
            ),
        ),
    ]

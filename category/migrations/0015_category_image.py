# Generated by Django 4.2.3 on 2023-10-01 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0014_delete_blogsubcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True,
                upload_to="photos/banner_category",
                verbose_name="عکس بنر برای صفحه اصلی",
            ),
        ),
    ]

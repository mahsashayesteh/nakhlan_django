# Generated by Django 4.2.3 on 2023-09-13 12:09

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogdetails",
            name="description",
            field=ckeditor.fields.RichTextField(default="null"),
        ),
        migrations.AddField(
            model_name="blogdetails",
            name="img_banner",
            field=models.ImageField(
                null=True,
                upload_to="blogs/blog_details_banner",
                verbose_name="تصویر بنر بلاگ",
            ),
        ),
        migrations.AddField(
            model_name="blogdetails",
            name="status",
            field=models.CharField(
                choices=[
                    ("disable", "غیرفعال"),
                    ("active", "فعال"),
                    ("editing", "در حال ویرایش"),
                ],
                default="disable",
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name="blogdetails",
            name="subject",
            field=ckeditor.fields.RichTextField(default="null"),
        ),
    ]

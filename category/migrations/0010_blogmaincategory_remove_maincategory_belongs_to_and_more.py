# Generated by Django 4.2.3 on 2023-09-16 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0009_maincategory_belongs_to"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogMainCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="null", max_length=100, verbose_name="نام"
                    ),
                ),
                ("slug", models.SlugField(max_length=100, unique=True)),
                (
                    "cat_image",
                    models.ImageField(
                        blank=True,
                        upload_to="photos/categories",
                        verbose_name="عکس دسته بندی",
                    ),
                ),
            ],
            options={
                "verbose_name": "blogsmaincategory",
                "verbose_name_plural": "blogs main categories",
            },
        ),
        migrations.RemoveField(
            model_name="maincategory",
            name="belongs_to",
        ),
        migrations.CreateModel(
            name="BlogSubCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="نام")),
                (
                    "slug",
                    models.SlugField(allow_unicode=True, max_length=100, unique=True),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.category",
                        verbose_name="دسته بندی",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="نام")),
                ("slug", models.SlugField(max_length=100, unique=True)),
                (
                    "main_category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.maincategory",
                        verbose_name="دسته بندی اصلی",
                    ),
                ),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
            },
        ),
    ]
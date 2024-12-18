# Generated by Django 4.2.1 on 2023-07-05 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
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
                    "full_address",
                    models.TextField(blank=True, max_length=500, verbose_name="آدرس"),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        upload_to="userprofile",
                        verbose_name="عکس پروفایل کاربر",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="کاربر",
                    ),
                ),
            ],
        ),
    ]

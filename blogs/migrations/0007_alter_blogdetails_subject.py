# Generated by Django 4.2.3 on 2023-09-15 18:21

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0006_blogdetails_category_blogdetails_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogdetails",
            name="subject",
            field=django_quill.fields.QuillField(
                db_collation="utf8_persian_ci", unique=True
            ),
        ),
    ]
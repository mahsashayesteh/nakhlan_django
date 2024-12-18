# Generated by Django 4.2.3 on 2023-09-13 17:50

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0004_blogdetails_img_banner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogdetails",
            name="description",
            field=django_quill.fields.QuillField(default="null"),
        ),
        migrations.AlterField(
            model_name="blogdetails",
            name="subject",
            field=django_quill.fields.QuillField(default="null"),
        ),
    ]

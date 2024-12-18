# Generated by Django 4.2.3 on 2023-07-13 07:48

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ("category", "0003_delete_subcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="parent",
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="category.category",
            ),
        ),
    ]

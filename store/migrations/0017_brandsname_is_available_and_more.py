# Generated by Django 4.2.3 on 2023-08-03 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0016_product_sub_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="brandsname",
            name="is_available",
            field=models.BooleanField(default=True, verbose_name="فعال است"),
        ),
        migrations.AlterField(
            model_name="variation",
            name="variation_category",
            field=models.CharField(
                choices=[("رنگ", "رنگ"), ("سایز", "سایز")],
                max_length=100,
                verbose_name="دسته بندی تنوع",
            ),
        ),
    ]
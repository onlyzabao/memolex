# Generated by Django 4.2 on 2023-04-20 23:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workspace", "0008_package_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="package",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
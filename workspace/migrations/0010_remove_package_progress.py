# Generated by Django 4.2 on 2023-04-29 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0009_alter_package_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='progress',
        ),
    ]

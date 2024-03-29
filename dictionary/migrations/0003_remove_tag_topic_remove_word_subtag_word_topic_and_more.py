# Generated by Django 4.2.1 on 2023-05-10 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dictionary", "0002_remove_word_tag_subtag_word_subtag"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tag",
            name="topic",
        ),
        migrations.RemoveField(
            model_name="word",
            name="subtag",
        ),
        migrations.AddField(
            model_name="word",
            name="topic",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="dictionary.topic",
            ),
        ),
        migrations.DeleteModel(
            name="SubTag",
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]

# Generated by Django 4.1.6 on 2023-02-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("page", "0004_alter_tag_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(max_length=10),
        ),
    ]

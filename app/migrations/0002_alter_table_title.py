# Generated by Django 4.2 on 2023-04-11 19:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="table",
            name="title",
            field=models.CharField(max_length=20),
        ),
    ]

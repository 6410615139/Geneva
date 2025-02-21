# Generated by Django 5.1.6 on 2025-02-21 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("map", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="result",
            name="rain",
        ),
        migrations.RemoveField(
            model_name="result",
            name="suggestion",
        ),
        migrations.AddField(
            model_name="result",
            name="rain_image",
            field=models.ImageField(blank=True, null=True, upload_to="rain/"),
        ),
        migrations.AddField(
            model_name="result",
            name="suggestion_image",
            field=models.ImageField(blank=True, null=True, upload_to="suggestion/"),
        ),
        migrations.AlterField(
            model_name="sector",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="sector/"),
        ),
    ]

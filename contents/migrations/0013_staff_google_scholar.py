# Generated by Django 4.1.2 on 2023-01-08 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0012_staff_about_alter_staff_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="google_scholar",
            field=models.URLField(blank=True, max_length=999),
        ),
    ]
# Generated by Django 5.1.5 on 2025-02-08 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0003_vote"),
    ]

    operations = [
        migrations.CreateModel(
            name="PendingUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nim", models.CharField(max_length=9, unique=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("token", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("attempts", models.IntegerField(default=0)),
            ],
        ),
    ]

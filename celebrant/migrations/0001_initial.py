# Generated by Django 5.2.1 on 2025-05-28 11:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="VideoTribute",
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
                ("contributor_name", models.CharField(max_length=100)),
                ("contributor_email", models.EmailField(max_length=254)),
                (
                    "relationship",
                    models.CharField(
                        help_text="How do you know the celebrant?", max_length=100
                    ),
                ),
                (
                    "video_file",
                    models.FileField(
                        help_text="Upload your video tribute", upload_to="videos/"
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        blank=True, help_text="Optional message to accompany your video"
                    ),
                ),
                (
                    "is_approved",
                    models.BooleanField(
                        default=False, help_text="Admin approval required"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]

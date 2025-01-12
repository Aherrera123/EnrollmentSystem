# Generated by Django 4.2.15 on 2025-01-11 10:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "ElementaryEnrollment",
            "0007_alter_section_current_students_alter_student_status",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="confirmation_code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.CreateModel(
            name="Announcements",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                ("date_posted", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

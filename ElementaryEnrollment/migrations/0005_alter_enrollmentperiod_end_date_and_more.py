# Generated by Django 4.2.15 on 2024-12-28 23:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ElementaryEnrollment", "0004_enrollmentperiod"),
    ]

    operations = [
        migrations.AlterField(
            model_name="enrollmentperiod",
            name="end_date",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="enrollmentperiod",
            name="start_date",
            field=models.DateTimeField(),
        ),
    ]

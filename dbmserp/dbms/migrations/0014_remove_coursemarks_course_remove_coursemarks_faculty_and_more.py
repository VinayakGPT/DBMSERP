# Generated by Django 5.1.2 on 2024-11-07 14:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dbms", "0013_coursemarks"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="coursemarks",
            name="course",
        ),
        migrations.RemoveField(
            model_name="coursemarks",
            name="faculty",
        ),
        migrations.CreateModel(
            name="FacultyCourseAssignment",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dbms.streamcourse",
                    ),
                ),
                (
                    "faculty",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="dbms.faculty"
                    ),
                ),
            ],
            options={
                "unique_together": {("faculty", "course")},
            },
        ),
        migrations.AddField(
            model_name="coursemarks",
            name="faculty_assignment",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="dbms.facultycourseassignment",
            ),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2.13 on 2024-11-08 08:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dbms", "0015_alter_facultycourseassignment_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="feedback",
            name="faculty",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="dbms.faculty",
            ),
            preserve_default=False,
        ),
    ]

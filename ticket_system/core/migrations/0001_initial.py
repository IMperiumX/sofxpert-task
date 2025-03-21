# Generated by Django 5.1.1 on 2025-03-12 22:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "0002_agent"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("unassigned", "Unassigned"),
                            ("assigned", "Assigned"),
                            ("sold", "Sold"),
                        ],
                        default="unassigned",
                        max_length=20,
                    ),
                ),
                ("description", models.TextField()),
                ("subject", models.CharField(max_length=100)),
                ("customer_name", models.CharField(max_length=100)),
                ("customer_email", models.EmailField(max_length=254)),
                (
                    "assigned_agent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tickets",
                        to="users.agent",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
    ]

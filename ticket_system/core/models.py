from django.db import models


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("unassigned", "Unassigned"),
        ("assigned", "Assigned"),
        ("sold", "Sold"),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_agent = models.ForeignKey(
        "users.Agent",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tickets",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unassigned",
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    subject = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Ticket {self.pk} - {self.status}"

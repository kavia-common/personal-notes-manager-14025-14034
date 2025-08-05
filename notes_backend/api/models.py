from django.db import models
from django.contrib.auth.models import User

# PUBLIC_INTERFACE
class Note(models.Model):
    """A single Note belonging to a user."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return f"{self.title} ({self.owner.username})"

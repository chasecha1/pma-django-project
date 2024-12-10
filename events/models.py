from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Model that defines what an event consists of in our application
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='events')
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    members = models.ManyToManyField(User, related_name="members_events", blank=True)  # Users who have joined the event
    requests = models.ManyToManyField(User, related_name="requested_events", blank=True)

    def __str__(self):
        return str(self.title)

class File(models.Model):
    event = models.ForeignKey(Event, related_name='files', on_delete=models.CASCADE)  # Each file belongs to one event
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='uploaded_files', 
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)  # New field for file description
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords for search", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure the user is assigned a default if not provided
        if not self.user:
            self.user = User.objects.get(id=1)  # Replace with the ID of a valid default user
        # Set title to the file name if not provided
        if not self.title and self.file:
            self.title = self.file.name
        super().save(*args, **kwargs)

    def get_keywords(self):
        return [keyword.strip() for keyword in self.keywords.split(',') if keyword.strip()]

    def __str__(self):
        return self.title

class Message(models.Model):
    event = models.ForeignKey(Event, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    related_name='uploaded_messages',
    on_delete=models.CASCADE
    )
    message = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

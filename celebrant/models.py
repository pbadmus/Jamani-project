from django.db import models

class RSVP(models.Model):
    ATTENDANCE_CHOICES = [
        ('yes', 'Yes, I will attend'),
        ('no', 'No, I cannot attend'),
        ('maybe', 'Maybe, not sure yet')
    ]
    
    # Guest Information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # RSVP Details
    attendance = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    number_of_guests = models.PositiveIntegerField(default=0, help_text="Number of additional guests (not including yourself)")
    
    # Special Requirements
    dietary_restrictions = models.TextField(blank=True, help_text="Any dietary restrictions or allergies")
    special_requests = models.TextField(blank=True, help_text="Any special requests or accommodations needed")
    
    # Message
    message = models.TextField(blank=True, help_text="Birthday message for the celebrant")
    
    # Relationship
    relationship = models.CharField(max_length=100, blank=True, help_text="How do you know Mr. Jamiu?")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"
    
    def __str__(self):
        return f"{self.name} - {self.get_attendance_display()}"
    
    @property
    def total_attendees(self):
        """Total number of people attending (including the person who RSVPed)"""
        if self.attendance == 'yes':
            return 1 + self.number_of_guests
        return 0

# Only model we need is for video uploads
class VideoTribute(models.Model):
    contributor_name = models.CharField(max_length=100)
    contributor_email = models.EmailField()
    relationship = models.CharField(max_length=100, help_text="How do you know the celebrant?")
    video_file = models.FileField(upload_to='videos/', help_text="Upload your video tribute")
    message = models.TextField(blank=True, help_text="Optional message to accompany your video")
    is_approved = models.BooleanField(default=False, help_text="Admin approval required")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Video from {self.contributor_name}"
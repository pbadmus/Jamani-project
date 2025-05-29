from django import forms
from .models import RSVP, VideoTribute

class VideoTributeForm(forms.ModelForm):
    class Meta:
        model = VideoTribute
        fields = ['contributor_name', 'contributor_email', 'relationship', 'video_file', 'message']
        widgets = {
            'contributor_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'contributor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'required': True
            }),
            'relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Friend, Colleague, Neighbor, Family',
                'required': True
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Optional: Add a message to accompany your video...'
            })
        }
    
    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video:
            # Check file size (limit to 100MB)
            if video.size > 100 * 1024 * 1024:
                raise forms.ValidationError("Video file too large. Please keep it under 100MB.")
            
            # Check file type
            allowed_types = ['video/mp4', 'video/avi', 'video/mov', 'video/wmv', 'video/webm']
            if video.content_type not in allowed_types:
                raise forms.ValidationError("Please upload a valid video file (MP4, AVI, MOV, WMV, or WebM).")
        
        return video

class RSVPForm(forms.ModelForm):
    class Meta:
        model= RSVP
        fields = [
            'name', 'email', 'phone', 'attendance', 'number_of_guests', 
            'dietary_restrictions', 'special_requests', 'message', 'relationship'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number (optional)'
            }),
            'attendance': forms.RadioSelect(attrs={
                'class': 'form-radio'
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 10,
                'placeholder': '0'
            }),
            'dietary_restrictions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Please list any dietary restrictions, allergies, or special meal requirements...'
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special accommodations or requests for the event...'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share a birthday message or memory for John...'
            }),
            'relationship': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Friend, Colleague, Family member, Neighbor'
            })
        }
    
    def clean_number_of_guests(self):
        attendance = self.cleaned_data.get('attendance')
        number_of_guests = self.cleaned_data.get('number_of_guests')
        
        if attendance == 'no' and number_of_guests > 0:
            raise forms.ValidationError("You cannot bring guests if you're not attending.")
        
        if number_of_guests < 0:
            raise forms.ValidationError("Number of guests cannot be negative.")
        
        if number_of_guests > 10:
            raise forms.ValidationError("Maximum 10 additional guests allowed.")
        
        return number_of_guests
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email already exists (optional -  might want to allow updates)
        if RSVP.objects.filter(email=email).exists():
            existing_rsvp = RSVP.objects.get(email=email)
            pass
        return email
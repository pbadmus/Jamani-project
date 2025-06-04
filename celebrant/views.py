from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from birthday_project import settings
from celebrant.forms import RSVPForm, VideoTributeForm
from celebrant.models import RSVP, VideoTribute

# Create your views here.


def home_page(request):
    """Homepage with static content and approved videos"""
    # Get approved video tributes for display
    video_tributes = VideoTribute.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    context = {
        'video_tributes': video_tributes,
    }
    return render(request, 'home.html', )
    


def upload_video(request):
    """Handle video tribute upload by visitors"""
    if request.method == 'POST':
        form = VideoTributeForm(request.POST, request.FILES)
        if form.is_valid():
            video_tribute = form.save()
            messages.success(request, 
                f'Thank you {video_tribute.contributor_name}! Your video tribute has been submitted and will be reviewed before being published.')
            return redirect('birthday_app:upload_video')
    else:
        form = VideoTributeForm()
    
    # Get recent approved videos for display
    recent_videos = VideoTribute.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    context = {
        'form': form,
        'recent_videos': recent_videos,
    }
    
    return render(request, 'upload_video.html', context)

def video_gallery(request):
    """Display all approved video tributes"""
    video_tributes = VideoTribute.objects.filter(is_approved=True).order_by('-created_at')
    
    context = {
        'video_tributes': video_tributes,
    }
    
    return render(request, 'video_gallery.html', context)

def rsvp_view(request):
    if request.method == "POST":
        form = RSVPForm(request.POST)
        if form.is_valid():
            # Check if RSVP already exists for this email
            email = form.cleaned_data['email']
            existing_rsvp = RSVP.objects.filter(email=email).first()
            
            if existing_rsvp:
                # Update existing RSVP
                for field, value in form.cleaned_data.items():
                    setattr(existing_rsvp, field, value)
                existing_rsvp.save()
                rsvp = existing_rsvp
                messages.success(request, f'Thank you {rsvp.name}! Your RSVP has been updated.')
            else:
                # Create new RSVP
                rsvp = form.save()
                messages.success(request, f'Thank you {rsvp.name}! Your RSVP has been received.')
            
            # Send confirmation email
            try:
                send_confirmation_email(rsvp)
            except Exception as e:
                # Don't fail the RSVP if email fails
                print(f"Failed to send confirmation email: {e}")
            
            return redirect('birthday_app:rsvp_success', rsvp_id=rsvp.id)
    else:
        form = RSVPForm()
    
    # Get some stats for display
    stats = {
        'total_attending': RSVP.objects.filter(attendance='yes').count(),
        'total_guests': sum(rsvp.total_attendees for rsvp in RSVP.objects.filter(attendance='yes')),
    }
    
    context = {
        'form': form,
        'stats': stats,
    }
    
    return render(request, 'rsvp.html', context)

def rsvp_success(request, rsvp_id):
    """RSVP success page"""
    rsvp = get_object_or_404(RSVP, id=rsvp_id)
    
    context = {
        'rsvp': rsvp,
    }
    
    return render(request, 'rsvp_success.html', context)

def send_confirmation_email(rsvp):
    """Send RSVP confirmation email"""
    if rsvp.attendance == 'yes':
        subject = "RSVP Confirmed - Jamiu Akanbi Yaya-Badmus's 60th Birthday Celebration"
        message = f"""
Dear {rsvp.name},

Thank you for confirming your attendance at Jamiu Akanbi Yaya-Badmus's 60th Birthday Celebration!

Event Details:
Date: Saturday, August 2, 2025
Time: 10:00 AM
Venue: Grand Ballroom, City Hotel
Address: wiill be communicated shortly

Your RSVP Details:
- Attendees: {rsvp.total_attendees} (including yourself)
- Dietary restrictions: {rsvp.dietary_restrictions or 'None specified'}
- Special requests: {rsvp.special_requests or 'None specified'}

We look forward to celebrating with you!

Best regards,
The Celebration Committee
        """
    elif rsvp.attendance == 'no':
        subject = "RSVP Received - Jamiu Akanbi Yaya-Badmus's 60th Birthday Celebration"
        message = f"""
Dear {rsvp.name},

Thank you for responding to the invitation for Jamiu Akanbi Yaya-Badmus's 60th Birthday Celebration.

We're sorry you won't be able to join us, but we appreciate you letting us know.

{f'Your message: "{rsvp.message}"' if rsvp.message else ''}

Best regards,
The Celebration Committee
        """
    else:  # maybe
        subject = "RSVP Received - Jamiu Akanbi Yaya-Badmus's 60th Birthday Celebration"
        message = f"""
Dear {rsvp.name},

Thank you for responding to the invitation for Jamiu Akanbi Yaya-Badmus's 60th Birthday Celebration.

We understand you're not sure yet. Please let us know as soon as you can confirm your attendance.

Event Details:
Date: Saturday, August 2, 2025
Time: 10:00 AM
Venue: Grand Ballroom, City Hotel

Best regards,
The Celebration Committee
        """
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [rsvp.email],
        fail_silently=False,
    )
    
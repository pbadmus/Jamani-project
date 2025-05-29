from django.contrib import admin
from django.db.models import Sum, Count

from .models import RSVP, VideoTribute

@admin.register(VideoTribute)
class VideoTributeAdmin(admin.ModelAdmin):
    list_display = ('contributor_name', 'relationship', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    search_fields = ('contributor_name', 'contributor_email', 'relationship')
    
    fieldsets = (
        ('Contributor Information', {
            'fields': ('contributor_name', 'contributor_email', 'relationship')
        }),
        ('Video Content', {
            'fields': ('video_file', 'message')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'created_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'attendance', 'total_attendees', 'relationship', 'created_at')
    list_filter = ('attendance', 'created_at')
    search_fields = ('name', 'email', 'relationship')
    readonly_fields = ('created_at', 'updated_at', 'total_attendees')
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('name', 'email', 'phone', 'relationship')
        }),
        ('RSVP Details', {
            'fields': ('attendance', 'number_of_guests', 'total_attendees')
        }),
        ('Special Requirements', {
            'fields': ('dietary_restrictions', 'special_requests')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    # Add summary statistics
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        
        metrics = {
            'total_rsvps': qs.count(),
            'attending': qs.filter(attendance='yes').count(),
            'not_attending': qs.filter(attendance='no').count(),
            'maybe_attending': qs.filter(attendance='maybe').count(),
            'total_guests': qs.filter(attendance='yes').aggregate(
                total=Sum('number_of_guests')
            )['total'] or 0,
            'total_attendees': qs.filter(attendance='yes').count() + (qs.filter(attendance='yes').aggregate(
                total=Sum('number_of_guests')
            )['total'] or 0),
        }
        
        response.context_data['summary'] = metrics
        return response
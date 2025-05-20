from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Event, EventCategory, EventSpeaker, EventRegistration

def event_list(request):
    events = Event.objects.filter(
        is_active=True,
        end_date__gte=timezone.now()
    ).order_by('start_date')
    
    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        events = events.filter(category__slug=category_slug)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    categories = EventCategory.objects.all()
    return render(request, 'events/event_list.html', {
        'events': events,
        'categories': categories
    })

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    registrations = EventRegistration.objects.filter(event=event, status='registered')
    
    return render(request, 'events/event_detail.html', {
        'event': event,
        'registrations': registrations
    })

@login_required
def event_register(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    
    # Check if user is already registered
    if EventRegistration.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, 'You are already registered for this event.')
        return redirect('events:event_detail', slug=slug)
    
    if request.method == 'POST':
        try:
            registration = EventRegistration.objects.create(
                user=request.user,
                event=event,
                status='registered'
            )
            messages.success(request, 'Registration submitted successfully!')
            return redirect('events:event_detail', slug=slug)
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'events/event_register.html', {'event': event})

def category_list(request):
    categories = EventCategory.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(EventCategory, slug=slug)
    events = Event.objects.filter(
        category=category,
        is_active=True,
        end_date__gte=timezone.now()
    ).order_by('start_date')
    
    return render(request, 'events/category_detail.html', {
        'category': category,
        'events': events
    })

def speaker_list(request):
    speakers = EventSpeaker.objects.all()
    return render(request, 'events/speaker_list.html', {'speakers': speakers})

def speaker_detail(request, pk):
    speaker = get_object_or_404(EventSpeaker, pk=pk)
    
    return render(request, 'events/speaker_detail.html', {
        'speaker': speaker,
    })

def event_calendar(request):
    events = Event.objects.filter(
        is_active=True,
        end_date__gte=timezone.now()
    ).order_by('start_date')
    
    return render(request, 'events/event_calendar.html', {'events': events})

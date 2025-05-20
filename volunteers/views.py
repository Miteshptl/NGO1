from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Volunteer, VolunteerOpportunity, VolunteerApplication, VolunteerHours

@login_required
def volunteer_register(request):
    if request.method == 'POST':
        try:
            volunteer = Volunteer.objects.create(
                user=request.user,
                skills=request.POST.get('skills'),
                interests=request.POST.get('interests'),
                availability=request.POST.get('availability'),
                status='pending'
            )
            messages.success(request, 'Volunteer registration submitted successfully!')
            return redirect('volunteers:volunteer_profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'volunteers/volunteer_register.html')

def opportunity_list(request):
    opportunities = VolunteerOpportunity.objects.filter(
        is_active=True,
        end_date__gt=timezone.now()
    ).order_by('deadline')
    return render(request, 'volunteers/opportunity_list.html', {'opportunities': opportunities})

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(VolunteerOpportunity, pk=pk, is_active=True)
    return render(request, 'volunteers/opportunity_detail.html', {'opportunity': opportunity})

@login_required
def apply_opportunity(request, pk):
    opportunity = get_object_or_404(VolunteerOpportunity, pk=pk, is_active=True)
    
    if request.method == 'POST':
        try:
            application = VolunteerApplication.objects.create(
                volunteer=request.user.volunteer,
                opportunity=opportunity,
                motivation=request.POST.get('motivation'),
                status='pending'
            )
            messages.success(request, 'Application submitted successfully!')
            return redirect('volunteers:volunteer_profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    return render(request, 'volunteers/apply_opportunity.html', {'opportunity': opportunity})

@login_required
def volunteer_profile(request):
    volunteer = get_object_or_404(Volunteer, user=request.user)
    applications = VolunteerApplication.objects.filter(volunteer=volunteer).order_by('-created_at')
    hours_logs = VolunteerHours.objects.filter(volunteer=volunteer).order_by('-date')
    
    return render(request, 'volunteers/volunteer_profile.html', {
        'volunteer': volunteer,
        'applications': applications,
        'hours_logs': hours_logs
    })

@login_required
def log_hours(request):
    if request.method == 'POST':
        try:
            hours_log = VolunteerHours.objects.create(
                volunteer=request.user.volunteer,
                opportunity_id=request.POST.get('opportunity'),
                hours=request.POST.get('hours'),
                date=request.POST.get('date'),
                description=request.POST.get('description')
            )
            messages.success(request, 'Hours logged successfully!')
            return redirect('volunteers:volunteer_profile')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    opportunities = VolunteerOpportunity.objects.filter(
        volunteerapplication__volunteer=request.user.volunteer,
        volunteerapplication__status='approved'
    ).distinct()
    
    return render(request, 'volunteers/log_hours.html', {'opportunities': opportunities})

@login_required
def hours_history(request):
    hours_logs = VolunteerHours.objects.filter(
        volunteer=request.user.volunteer
    ).order_by('-date')
    
    return render(request, 'volunteers/hours_history.html', {'hours_logs': hours_logs})

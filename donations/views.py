from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Donation, DonationCampaign, RecurringDonation

@login_required
def donate(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        try:
            donation = Donation.objects.create(
                donor=request.user,
                amount=amount,
                is_anonymous=is_anonymous,
                payment_status='completed'
            )
            messages.success(request, 'Thank you for your donation!')
            return redirect('donations:donation_success')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    return render(request, 'donations/donate.html')

def campaign_list(request):
    campaigns = DonationCampaign.objects.filter(is_active=True)
    return render(request, 'donations/campaign_list.html', {'campaigns': campaigns})

def campaign_detail(request, pk):
    campaign = get_object_or_404(DonationCampaign, pk=pk, is_active=True)
    donations = Donation.objects.filter(project=campaign, payment_status='completed')
    return render(request, 'donations/campaign_detail.html', {
        'campaign': campaign,
        'donations': donations
    })

@login_required
def recurring_donation(request):
    if request.method == 'POST':
        campaign_id = request.POST.get('campaign')
        amount = request.POST.get('amount')
        frequency = request.POST.get('frequency')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        try:
            campaign = DonationCampaign.objects.get(id=campaign_id)
            recurring = RecurringDonation.objects.create(
                donor=request.user,
                project=campaign.project if hasattr(campaign, 'project') else None,
                amount=amount,
                frequency=frequency,
                is_anonymous=is_anonymous,
                status='active'
            )
            messages.success(request, 'Recurring donation set up successfully!')
            return redirect('donations:donation_success')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
    
    campaigns = DonationCampaign.objects.filter(is_active=True)
    return render(request, 'donations/recurring_donation.html', {'campaigns': campaigns})

@login_required
def donation_history(request):
    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    recurring = RecurringDonation.objects.filter(donor=request.user).order_by('-created_at')
    
    return render(request, 'donations/donation_history.html', {
        'donations': donations,
        'recurring': recurring
    })

def donation_success(request):
    return render(request, 'donations/donation_success.html')

def donation_cancel(request):
    return render(request, 'donations/donation_cancel.html')

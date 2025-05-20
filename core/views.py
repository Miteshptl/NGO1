from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project, TeamMember, Testimonial, FAQ, SiteSettings
from django.contrib.auth.decorators import login_required
from blog.models import Post
from blog.forms import PostForm
from core.forms import ProjectForm

def home(request):
    projects = Project.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    site_settings = SiteSettings.objects.first()
    
    context = {
        'projects': projects,
        'testimonials': testimonials,
        'team_members': team_members,
        'site_settings': site_settings,
    }
    return render(request, 'core/home.html', context)

def about(request):
    team_members = TeamMember.objects.filter(is_active=True)
    testimonials = Testimonial.objects.filter(is_active=True)
    site_settings = SiteSettings.objects.first()
    
    context = {
        'team_members': team_members,
        'testimonials': testimonials,
        'site_settings': site_settings,
    }
    return render(request, 'core/about.html', context)

def project_list(request):
    projects = Project.objects.filter(is_active=True)
    return render(request, 'core/project_list.html', {'projects': projects})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    return render(request, 'core/project_detail.html', {'project': project})

def team(request):
    team_members = TeamMember.objects.filter(is_active=True)
    return render(request, 'core/team.html', {'team_members': team_members})

def testimonials(request):
    testimonials = Testimonial.objects.filter(is_active=True)
    return render(request, 'core/testimonials.html', {'testimonials': testimonials})

def faq(request):
    faqs = FAQ.objects.filter(is_active=True)
    return render(request, 'core/faq.html', {'faqs': faqs})

def contact(request):
    site_settings = SiteSettings.objects.first()
    
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        # For now, we'll just show a success message
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
    
    return render(request, 'core/contact.html', {'site_settings': site_settings})

@login_required
def profile(request):
    user = request.user
    profile = getattr(user, 'userprofile', None)
    return render(request, 'core/profile.html', {'user': user, 'profile': profile})

@login_required
def dashboard(request):
    content_type = request.GET.get('content_type', 'blog')
    post_form = PostForm()
    project_form = ProjectForm()
    success_message = None

    if request.method == 'POST':
        if 'add_blog' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                post.save()
                success_message = 'Blog post added successfully!'
                post_form = PostForm()  # reset form
        elif 'add_project' in request.POST:
            project_form = ProjectForm(request.POST, request.FILES)
            if project_form.is_valid():
                project = project_form.save(commit=False)
                project.created_by = request.user
                project.save()
                success_message = 'Project added successfully!'
                project_form = ProjectForm()  # reset form

    context = {
        'content_type': content_type,
        'post_form': post_form,
        'project_form': project_form,
        'success_message': success_message,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            form.save_m2m()
            return redirect('core:projects')
    else:
        form = ProjectForm()
    return render(request, 'core/add_project.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    tags = Tag.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 9)  # Show 9 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'tags': tags,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    context = {
        'post': post,
    }
    return render(request, 'blog/post_detail.html', context)

def category_detail(request, slug):
    # Optionally, you can remove or disable the category_detail view entirely if you don't want category pages.
    pass

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, is_published=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tag_detail.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            is_published=True
        ).order_by('-created_at')
    else:
        posts = Post.objects.none()
    
    # Pagination
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search.html', context)

@login_required
def add_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('blog:post_list')
    else:
        form = PostForm()
    return render(request, 'blog/add_blog.html', {'form': form})

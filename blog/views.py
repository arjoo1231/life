
from django.shortcuts import render
from django.db.models import Count
from . import models

def home(request):
    latest_posts = models.Post.objects.filter(status=models.Post.PUBLISHED).order_by('-published')[:3]
    
    context = {
        
        'latest_posts': latest_posts
    }

    return render(request, 'blog/home.html', context)

from .models import Post
from .models import Topic
from django.db.models import Count
from blog import models

def base_context(request):
    authors = Post.objects.filter(status='published').values_list('author__first_name', flat=True).distinct().order_by('author__first_name')
    return {'authors': authors}

def base_context(request):
    top_topics = Topic.objects.annotate(post_count=Count('posts')).order_by('-post_count')[:5]
    return {'top_topics': top_topics}
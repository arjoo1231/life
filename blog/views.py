
from django.shortcuts import render
from django.db.models import Count
from . import models
from .models import  Topic


def home(request):
    latest_posts = models.Post.objects.filter(status=models.Post.PUBLISHED).order_by('-published')[:3]
    topics = Topic.objects.all()  
    topic_data = []

    for topic in topics:
        post_count = topic.post_set.count() 
        topic_data.append({'topic': topic, 'post_count': post_count})

    sorted_data = sorted(topic_data, key=lambda x: x['post_count'], reverse=True)
    top_10_topics = sorted_data[:10]

    
    context = {

        'top_10_topics': top_10_topics,

        'latest_posts': latest_posts
    }

    return render(request, 'blog/home.html', context)

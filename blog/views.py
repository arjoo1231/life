
from django.shortcuts import render
from django.db.models import Count
from . import models
from .models import  Topic
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Topic, Post
from django.views import View
from django.views.generic.base import TemplateView


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


class TopicListView(ListView):
    model = models.Topic
    template_name = 'blog/topic_list.html'
    context_object_name = 'topic_list'

    
    def get_queryset(self):
       
        return Topic.objects.all().order_by('name')
    



    

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'blog/topic_detail.html'
    context_object_name = 'topic'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.get_object()
        related_posts = Post.objects.filter(topic=topic, status=Post.PUBLISHED).order_by('-published')
        context['related_posts'] = related_posts
        return context
    

class AboutView(View):
    def get(self, request):
        return render(request, 'blog/about.html')
    
class AboutView(TemplateView):

    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Post.objects.filter(status='published').values_list('author__first_name', flat=True).distinct().order_by('author__first_name')
        return context
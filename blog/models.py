from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse


class PostManager(models.Manager):
    def published(self):
        return self.filter(status='published')

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('topic-detail', args=[str(self.slug)])

    def post_count(self):
        return self.posts.filter(status='published').count()
    

class Post(models.Model):

    objects = PostManager()


    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(
        null=False,
        blank=True,
        help_text='The date & time this article was published'
    )
    DRAFT = 'draft'
    PUBLISHED = 'published'
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT,  
        related_name='blog_posts',
        null=False,
    )
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )   
    topics = models.ManyToManyField(Topic, blank=True, related_name='posts') 

    def get_authors(self):
        return self.author

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    text = models.TextField()
    approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'this comment is done by {self.name} on "{self.post.title}"'

    class Meta:
        ordering = ['-created']


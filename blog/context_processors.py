from .models import Post

def base_context(request):
    authors = Post.objects.filter(status='published').values_list('author__first_name', flat=True).distinct().order_by('author__first_name')
    return {'authors': authors}
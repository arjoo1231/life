from django.http import HttpResponse


def index(request):
    return HttpResponse("Time, as I've discovered, is a precious resource that should not be wasted.")
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def index(request):
    return render(request, 'restaurants/register.html')
    # return "Hello World!"
    # template = loader.get_template('restaurants/index.html')
    # return HttpResponse(template.render(request))
    # return HttpResponse("Hello, world. You're at the polls index.")

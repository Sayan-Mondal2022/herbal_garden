from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "main/home.html")

def connect(request):
    return render(request, "main/connect.html")

def blog(request):
    return render(request, "main/blog.html")
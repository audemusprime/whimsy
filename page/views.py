from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def signup(request):
    error_msg = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            error_msg = "Invalid credentials - try again"
    form = UserCreationForm()
    context = {"form": form, "error": error_msg}
    return render(request, "registration/signup.html", context)


def pages(request):
    pages = Page.objects.filter(user=request.user)
    # iterate through the pages and retrieve associated tags
    for page in pages:
        if page.tags.count():
            assoc_tags = page.tags.all()
    return render(request, "page/list.html", {"pages": pages, "tags": assoc_tags})

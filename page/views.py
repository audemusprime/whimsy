from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *

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
    return render(request, "page/list.html", {"pages": pages})


def detail(request, page_id):
    page = Page.objects.get(id=page_id)
    tags = page.tags.all()
    blocks = page.blocks.all()
    return render(
        request,
        "page/detail.html",
        {
            "page": page,
            "tags": tags,
            "blocks": blocks,
        },
    )


def update_page(request, page_id):
    page = Page.objects.get(id=page_id)
    query = page.blocks.all()
    tags = page.tags.all()
    new_tag = TagForm()
    if request.method == "POST":
        formset = BlockFormset(request.POST, queryset=query)
        if formset.is_valid():
            for form in formset.forms:
                form.instance.page_id = page_id
            formset.save()
            return redirect("detail", page_id=page_id)
    else:
        formset = BlockFormset(queryset=query)
    context = {
        "page": page,
        "formset": formset,
        "tags": tags,
        "new_tag": new_tag,
    }
    return render(request, "page/update.html", context)


@csrf_exempt
def add_tag(request, page_id):
    page = Page.objects.get(id=page_id)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            added_tag = form.save(commit=True)
            added_tag.page.add(page)
            added_tag.save()
    return JsonResponse({"status": "success"})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
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


@login_required
def pages(request):
    pages = Page.objects.filter(user=request.user)
    return render(request, "page/list.html", {"pages": pages})


@login_required
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


@login_required
def create_page(request):
    formset = BlockFormset(queryset=Block.objects.none())
    title_form = TitleForm()
    user = request.user
    if request.method == "POST":
        title_form = TitleForm(request.POST)
        formset = BlockFormset(request.POST)
        if title_form.is_valid() and formset.is_valid():
            title_form.instance.user_id = user.id
            page = title_form.save()
            blocks = formset.save(commit=False)
            for block in blocks:
                block.page_id = page.id
                block.save()
            return redirect("detail", page_id=page.id)
    context = {
        "title_form": title_form,
        "formset": formset,
    }
    return render(request, "page/create.html", context)


@login_required
def update_page(request, page_id):
    page = Page.objects.get(id=page_id)
    query = page.blocks.all()
    tags = page.tags.all()
    new_tag = TagForm()
    if request.method == "POST":
        formset = BlockFormset(request.POST, queryset=query)
        title_form = TitleForm(request.POST, instance=page)

        if title_form.is_valid() and formset.is_valid():
            obj = title_form.save()
            blocks = formset.save(commit=False)
            for form in blocks:
                form.page_id = obj.id
                form.save()
                return redirect("detail", page_id=page_id)
    else:
        formset = BlockFormset(queryset=query)
        title_form = TitleForm(instance=page)
    context = {
        "page": page,
        "formset": formset,
        "title_form": title_form,
        "tags": tags,
        "new_tag": new_tag,
    }
    return render(request, "page/update.html", context)


@login_required
def delete_page(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    page.delete()
    return redirect("pages")


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

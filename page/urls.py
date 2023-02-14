from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("accounts/signup/", views.signup, name="signup"),
    path("pages/", views.pages, name="pages"),
    path("pages/<str:page_id>/", views.detail, name="detail"),
]

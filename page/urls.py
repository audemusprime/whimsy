from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("accounts/signup/", views.signup, name="signup"),
    path("pages/", views.pages, name="pages"),
    path("pages/<str:page_id>/", views.detail, name="detail"),
    path("pages/<str:page_id>/add_tag", views.add_tag, name="add_tag"),
    path("pages/create", views.create_page, name="create"),
    path(
        "pages/<str:page_id>/update",
        views.update_page,
        name="update_page",
    ),
]

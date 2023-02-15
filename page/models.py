from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import shortuuid
from shortuuid.django_fields import ShortUUIDField


# Create your models here.
class Page(models.Model):
    id = ShortUUIDField(
        primary_key=True,
        auto_created=True,
        unique=True,
        length=10,
        alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Untitled")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"page_id": self.id})


class Block(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="blocks")
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Block %s from %s page" % (self.id, self.page)


class Tag(models.Model):
    page = models.ManyToManyField(Page, related_name="tags")
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

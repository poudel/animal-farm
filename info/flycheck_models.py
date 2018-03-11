from django.db import models
from django.conf import settings
from gears.models import BaseModel


class KbTag(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.slug


class KbArticle(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(KbTag, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

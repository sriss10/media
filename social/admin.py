from django.contrib import admin
from . import models
# Register your models here.
admin.site.register([
    models.Post,
    models.Comment,
    models.Friends,
    models.Like
])

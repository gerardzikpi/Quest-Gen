from django.contrib import admin
from .models import Course, Topic, Question

# Register your models here.

admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Question)

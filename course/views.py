from django.views.generic import ListView
from .models import Course


class IndexView(ListView):
    model = Course
    template_name = "course/index.html"
    context_object_name = "courses"

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Lesson


class IndexView(ListView):
    model = Course
    template_name = "course/index.html"
    context_object_name = "courses"


class CourseDetailView(DetailView):
    model = Course
    template_name = "course/course_detail.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lessons"] = self.object.lessons.all()
        return context

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        return get_object_or_404(Course, pk=course_pk)


class LessonDetailView(DetailView):
    model = Lesson
    template_name = "course/lesson_detail.html"
    context_object_name = "lesson"

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        lesson_pk = self.kwargs.get("lesson_pk")
        return get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)

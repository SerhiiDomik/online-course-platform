from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Course, Lesson


class PosterView(TemplateView):
    template_name = "course/poster.html"


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


class RegisterView(TemplateView):
    template_name = "course/register.html"

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("course:index")
        return render(request, self.template_name, {"form": form})


class LoginView(TemplateView):
    template_name = "course/login.html"

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("course:index")
        return render(request, self.template_name, {"form": form})

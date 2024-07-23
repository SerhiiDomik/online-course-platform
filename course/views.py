from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView

from .forms import CustomUserCreationForm
from .models import Course, Lesson, User, SavedCourse


class PosterView(TemplateView):
    template_name = "course/poster.html"


class CourseListView(ListView):
    model = Course
    template_name = "course/course_list.html"
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()
        context["extra_material"] = lesson.extra_material if hasattr(lesson, "extra_material") else None
        return context

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        if 'mark_completed' in request.POST:
            request.user.mark_lesson_completed(lesson)
        return redirect('course:lesson-detail', course_pk=lesson.course.pk, lesson_pk=lesson.pk)


class RegisterView(TemplateView):
    template_name = "course/register.html"

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("course:course-list")
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
            return redirect("course:course-list")
        return render(request, self.template_name, {"form": form})


class SavedCourseListView(ListView):
    model = Course
    template_name = "course/saved_courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        return self.request.user.saved_courses.all()


@login_required
def save_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    SavedCourse.objects.get_or_create(user=request.user, course=course)
    return redirect('course:course-detail', course_pk=course_pk)


@login_required
def remove_course(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)
    SavedCourse.objects.filter(user=request.user, course=course).delete()
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', '/'))
    return redirect(next_url)

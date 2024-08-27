from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView

from .forms import (
    CustomUserCreationForm,
    LessonForm,
    CourseForm,
    CourseSearchForm,
)
from .models import Course, Lesson, SavedCourse


class PosterView(generic.TemplateView):
    template_name = "course/poster.html"


class CourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    queryset = Course.objects.all()
    template_name = "course/course_list.html"
    context_object_name = "courses"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CourseSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = CourseSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(name__icontains=form.cleaned_data["name"])
        return self.queryset


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
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


class CourseCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CourseForm
    template_name = "course/course_form.html"
    success_url = reverse_lazy("course:course-list")

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        return get_object_or_404(Course, course_id=course_pk)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = CourseForm
    template_name = "course/course_form.html"

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        course = get_object_or_404(Course, id=course_pk)
        if self.request.user != course.created_by:
            raise PermissionDenied("You are not allowed to edit this course.")
        return course

    def get_success_url(self):
        course_pk = self.kwargs.get("course_pk")
        return reverse_lazy("course:course-detail", kwargs={"course_pk": course_pk})


class CourseDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Course
    template_name = "course/course_confirm_delete.html"
    success_url = reverse_lazy("course:course-list")

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        course = get_object_or_404(Course, id=course_pk)
        if self.request.user != course.created_by:
            raise PermissionDenied("You are not allowed to delete this course.")
        return course


class LessonDetailView(LoginRequiredMixin, generic.DetailView):
    model = Lesson
    template_name = "course/lesson_detail.html"
    context_object_name = "lesson"

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        lesson_pk = self.kwargs.get("lesson_pk")
        return get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)

    def post(self, request, *args, **kwargs):
        lesson = self.get_object()
        if "mark_completed" in request.POST:
            request.user.mark_lesson_completed(lesson)
        return redirect(
            "course:lesson-detail", course_pk=lesson.course.pk, lesson_pk=lesson.pk
        )


class LessonCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = LessonForm
    template_name = "course/lesson_form.html"

    def form_valid(self, form):
        course = get_object_or_404(Course, pk=self.kwargs.get("course_pk"))
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "course:course-detail", kwargs={"course_pk": self.kwargs.get("course_pk")}
        )


class LessonUpdateView(LoginRequiredMixin, generic.UpdateView):
    form_class = LessonForm
    template_name = "course/lesson_form.html"

    def get_object(self, **kwargs):
        course_pk = self.kwargs.get("course_pk")
        lesson_pk = self.kwargs.get("lesson_pk")
        lesson = get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)
        if self.request.user != lesson.course.created_by:
            raise PermissionDenied("You are not allowed to edit this lesson.")
        return lesson

    def get_success_url(self):
        return reverse_lazy(
            "course:course-detail", kwargs={"course_pk": self.kwargs.get("course_pk")}
        )


class LessonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Lesson
    template_name = "course/lesson_confirm_delete.html"

    def get_object(self, queryset=None):
        course_pk = self.kwargs.get("course_pk")
        lesson_pk = self.kwargs.get("lesson_pk")
        lesson = get_object_or_404(Lesson, pk=lesson_pk, course_id=course_pk)
        if self.request.user != lesson.course.created_by:
            raise PermissionDenied("You are not allowed to edit this lesson.")
        return lesson

    def get_success_url(self):
        return reverse_lazy(
            "course:course-detail", kwargs={"course_pk": self.kwargs.get("course_pk")}
        )


class RegisterView(generic.TemplateView):
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


class LoginView(generic.TemplateView):
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


class SavedCourseListView(LoginRequiredMixin, generic.ListView):
    model = Course
    template_name = "course/saved_courses.html"
    context_object_name = "saved_courses"

    def get_queryset(self):
        return SavedCourse.objects.filter(user=self.request.user).order_by("-saved_at")


class SaveCourseView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs["course_pk"])
        SavedCourse.objects.get_or_create(user=request.user, course=course)
        return redirect("course:course-detail", course_pk=course.pk)


class RemoveCourseView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs["course_pk"])
        SavedCourse.objects.filter(user=request.user, course=course).delete()
        next_url = request.POST.get("next", request.META.get("HTTP_REFERER", "/"))
        return redirect(next_url)

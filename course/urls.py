from django.urls import path
from .views import (
    IndexView,
    CourseDetailView,
    LessonDetailView,
    PosterView,
    RegisterView,
    LoginView
)


app_name = "course"

urlpatterns = [
    path("", PosterView.as_view(), name="poster"),
    path("course/", IndexView.as_view(), name="index"),
    path(
        "course/<int:course_pk>/",
        CourseDetailView.as_view(),
        name="course-detail"
    ),
    path(
        "course/<int:course_pk>/lesson/<int:lesson_pk>/",
        LessonDetailView.as_view(),
        name="lesson-detail"
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]

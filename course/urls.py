from django.urls import path
from .views import IndexView, CourseDetailView, LessonDetailView


app_name = "course"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "course/<int:course_pk>/",
        CourseDetailView.as_view(),
        name="course-detail"
    ),
    path(
        "course/<int:course_pk>/lesson/<int:lesson_pk>/",
        LessonDetailView.as_view(),
        name="lesson-detail"
    )
]

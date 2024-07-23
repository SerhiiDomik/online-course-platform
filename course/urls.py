from django.urls import path
from .views import (
    CourseDetailView,
    LessonDetailView,
    PosterView,
    RegisterView,
    LoginView,
    LogoutView,
    CourseListView,
    save_course,
    remove_course,
    SavedCourseListView,
)


app_name = "course"

urlpatterns = [
    path("", PosterView.as_view(), name="poster"),
    path("course/", CourseListView.as_view(), name="course-list"),
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
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("saved-courses/", SavedCourseListView.as_view(), name="saved-courses-list"),
    path("course/<int:course_pk>/save/", save_course, name="save-course"),
    path("course/<int:course_pk>/remove/", remove_course, name="remove-saved-course"),
]

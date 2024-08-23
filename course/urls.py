from django import views
from django.urls import path
from .views import (
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    LessonDetailView,
    PosterView,
    RegisterView,
    LoginView,
    LogoutView,
    CourseListView,
    SaveCourseView,
    RemoveCourseView,
    SavedCourseListView,
    CourseDeleteView,
    LessonCreateView,
    LessonUpdateView,
    LessonDeleteView,
)


app_name = "course"

urlpatterns = [
    path("", PosterView.as_view(), name="poster"),
    path("course/", CourseListView.as_view(), name="course-list"),
    path("course/create/", CourseCreateView.as_view(), name="course-create"),
    path(
        "course/<int:course_pk>/update/",
        CourseUpdateView.as_view(),
        name="course-update"
    ),
    path(
        "course/<int:course_pk>/delete/",
        CourseDeleteView.as_view(),
        name="course-delete"
    ),
    path(
        "course/<int:course_pk>/",
        CourseDetailView.as_view(),
        name="course-detail"
    ),
    path(
        "course/<int:course_pk>/create-lesson/",
        LessonCreateView.as_view(),
        name="lesson-create"
    ),
    path(
        "course/<int:course_pk>/lesson/<int:lesson_pk>/",
        LessonDetailView.as_view(),
        name="lesson-detail"
    ),
    path(
        "course/<int:course_pk>/lesson/<int:lesson_pk>/update/",
        LessonUpdateView.as_view(),
        name="lesson-update"
    ),
    path(
        "course/<int:course_pk>/lesson/<int:lesson_pk>/delete/",
        LessonDeleteView.as_view(),
        name="lesson-delete"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("saved-courses/", SavedCourseListView.as_view(), name="saved-courses-list"),
    path("course/<int:course_pk>/save/", SaveCourseView.as_view(), name="save-course"),
    path("course/<int:course_pk>/remove/", RemoveCourseView.as_view(), name="remove-saved-course"),
]

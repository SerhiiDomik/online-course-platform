from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Course, Lesson


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ("username", "email",)
    list_filter = ("username",)
    list_display = UserAdmin.list_display + ("username",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course")
    list_filter = ("course",)

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    saved_courses = models.ManyToManyField("Course", through="SavedCourse", related_name="saved_by_users", blank=True)
    finished_lessons = models.ManyToManyField("Lesson", related_name="users_finished_lessons", blank=True)

    def mark_lesson_completed(self, lesson):
        self.finished_lessons.add(lesson)
        self.save()


class Course(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_creator")

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title


class SavedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_course_user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="saved_course_course")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-saved_at",)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"

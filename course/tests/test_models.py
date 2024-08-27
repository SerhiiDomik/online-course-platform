from django.test import TestCase

from course.models import User, Course, Lesson, SavedCourse


class UserModelTests(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(username="testuser", password="TestPass252215")
        self.assertEqual(str(user), "testuser")

    def test_mark_lesson_completed(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        course = Course.objects.create(
            name="Test Course", description="Test Course Description", created_by=user
        )
        lesson = Lesson.objects.create(
            title="Test Lesson", content="Test Lesson Content", course=course
        )
        user.mark_lesson_completed(lesson)
        self.assertIn(lesson, user.finished_lessons.all())


class CourseModelTests(TestCase):
    def test_course_str(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        course = Course.objects.create(
            name="Test Course", description="Test Course Description", created_by=user
        )
        self.assertEqual(str(course), "Test Course")


class LessonModelTests(TestCase):
    def test_lesson_str(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        course = Course.objects.create(
            name="Test Course", description="Test Course Description", created_by=user
        )
        lesson = Lesson.objects.create(
            title="Test Lesson", content="Test Lesson Content", course=course
        )
        self.assertEqual(str(lesson), "Test Lesson")


class SavedCourseModelTests(TestCase):
    def test_saved_course_str(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        course = Course.objects.create(
            name="Test Course", description="Test Course Description", created_by=user
        )
        saved_course = SavedCourse.objects.create(user=user, course=course)
        self.assertEqual(str(saved_course), f"{user.username} - {course.name}")

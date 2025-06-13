from django.test import TestCase
from django.urls import reverse
from course.models import Course, Lesson
from django.contrib.auth import get_user_model

User = get_user_model()


class LessonViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser", password="Password123_"
        )
        self.other_user = User.objects.create_user(
            username="OtherUser", password="Password123_"
        )
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", created_by=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson", content="Test Content", course=self.course
        )

    def test_lesson_detail_view(self):
        self.client.login(username="TestUser", password="Password123_")
        response = self.client.get(
            reverse(
                "course:lesson-detail",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course/lesson_detail.html")
        self.assertEqual(response.context["lesson"], self.lesson)

    def test_lesson_detail_view_not_authenticated(self):
        response = self.client.get(
            reverse(
                "course:lesson-detail",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_lesson_create_view(self):
        self.client.login(username="TestUser", password="Password123_")
        form_data = {
            "title": "New Lesson",
            "content": "New Lesson Content",
        }
        response = self.client.post(
            reverse("course:lesson-create", kwargs={"course_pk": self.course.pk}),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        new_lesson = Lesson.objects.get(title=form_data["title"])
        self.assertEqual(new_lesson.course, self.course)

    def test_lesson_create_view_not_authenticated(self):
        form_data = {
            "title": "New Lesson",
            "content": "New Lesson Content",
        }
        response = self.client.post(
            reverse("course:lesson-create", kwargs={"course_pk": self.course.pk}),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)

    def test_lesson_update_view(self):
        self.client.login(username="TestUser", password="Password123_")
        form_data = {
            "title": "Updated Lesson",
            "content": "Updated Lesson Content",
        }
        response = self.client.post(
            reverse(
                "course:lesson-update",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, form_data["title"])

    def test_lesson_update_view_not_authenticated(self):
        form_data = {
            "title": "Updated Lesson",
            "content": "Updated Lesson Content",
        }
        response = self.client.post(
            reverse(
                "course:lesson-update",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 302)

    def test_only_creator_can_update_lesson(self):
        self.client.login(username="OtherUser", password="Password123_")
        form_data = {
            "title": "Unauthorized Update",
            "content": "This update should not be allowed.",
        }
        response = self.client.post(
            reverse(
                "course:lesson-update",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            ),
            data=form_data,
        )
        self.assertEqual(response.status_code, 403)
        self.lesson.refresh_from_db()
        self.assertNotEqual(self.lesson.title, form_data["title"])

    def test_lesson_delete_view(self):
        self.client.login(username="TestUser", password="Password123_")
        response = self.client.post(
            reverse(
                "course:lesson-delete",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            )
        )
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(pk=self.lesson.pk)

    def test_lesson_delete_view_not_authenticated(self):
        response = self.client.post(
            reverse(
                "course:lesson-delete",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_only_creator_can_delete_lesson(self):
        self.client.login(username="OtherUser", password="Password123_")
        response = self.client.post(
            reverse(
                "course:lesson-delete",
                kwargs={"course_pk": self.course.pk, "lesson_pk": self.lesson.pk},
            )
        )
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Lesson.objects.filter(pk=self.lesson.pk).exists())

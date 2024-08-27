from django.test import TestCase
from django.urls import reverse

from course.forms import CustomUserCreationForm, CourseForm, LessonForm
from course.models import User, Course


class FormTests(TestCase):

    def test_custom_user_creation_form_valid(self):
        form_data = {
            'username': 'TestUser',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'Password123!',
            'password2': 'Password123!',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_course_form_valid(self):
        form_data = {
            'name': 'Test Course',
            'description': 'This is a test course.'
        }
        form = CourseForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_lesson_form_valid(self):
        course = Course.objects.create(
            name='Test Course',
            description='Test description',
            created_by=User.objects.create_user(username='TestUser')
        )
        form_data = {
            'title': 'Test Lesson',
            'content': 'This is the content of the test lesson.',
            'course': course.id
        }
        form = LessonForm(data=form_data)
        self.assertTrue(form.is_valid())
        lesson_instance = form.save(commit=False)

        lesson_instance.course = course

        lesson_instance.save()

        self.assertEqual(lesson_instance.title, 'Test Lesson')
        self.assertEqual(lesson_instance.content, 'This is the content of the test lesson.')
        self.assertEqual(lesson_instance.course, course)


class TestCourseSearchForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

        self.course1 = Course.objects.create(
            name="Python for Beginners",
            description="A beginner's course on Python programming.",
            created_by=self.user
        )
        self.course2 = Course.objects.create(
            name="Advanced Django",
            description="An advanced course on Django web development.",
            created_by=self.user
        )
        self.course3 = Course.objects.create(
            name="Python for Data Science",
            description="Python for data science applications.",
            created_by=self.user
        )

        self.client.force_login(self.user)

    def test_search_course_by_name(self):
        response = self.client.get(reverse("course:course-list"), {"name": "Python for Beginners"})
        self.assertContains(response, self.course1.name)
        self.assertNotContains(response, self.course2.name)
        self.assertNotContains(response, self.course3.name)

    def test_search_partial_course_name(self):
        response = self.client.get(reverse("course:course-list"), {"name": "Python"})
        self.assertContains(response, self.course1.name)
        self.assertContains(response, self.course3.name)
        self.assertNotContains(response, self.course2.name)

    def test_search_no_results(self):
        response = self.client.get(reverse("course:course-list"), {"name": "Ruby"})
        self.assertNotContains(response, self.course1.name)
        self.assertNotContains(response, self.course2.name)
        self.assertNotContains(response, self.course3.name)

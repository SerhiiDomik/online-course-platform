from django.contrib.auth import get_user_model
from django.test import TestCase
from course.models import SavedCourse, Course
from django.urls import reverse
from django.utils import timezone


User = get_user_model()


class SavedCourseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUser',
            password='Password123_'
        )
        self.client.force_login(self.user)

        self.course1 = Course.objects.create(name='Course 1', description='Description 1', created_by=self.user)
        self.course2 = Course.objects.create(name='Course 2', description='Description 2', created_by=self.user)

    def test_saved_course_list_view(self):
        SavedCourse.objects.create(user=self.user, course=self.course1, saved_at=timezone.now())

        response = self.client.get(reverse('course:saved-courses-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/saved_courses.html')
        self.assertIn('saved_courses', response.context)

        saved_courses = response.context['saved_courses']
        self.assertTrue(saved_courses.filter(course=self.course1).exists())
        self.assertFalse(saved_courses.filter(course=self.course2).exists())

    def test_save_course_view(self):
        response = self.client.post(reverse('course:save-course', kwargs={'course_pk': self.course2.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SavedCourse.objects.filter(user=self.user, course=self.course2).exists())

    def test_remove_course_view(self):
        SavedCourse.objects.create(user=self.user, course=self.course1, saved_at=timezone.now())

        response = self.client.post(reverse('course:remove-saved-course', kwargs={'course_pk': self.course1.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(SavedCourse.objects.filter(user=self.user, course=self.course1).exists())

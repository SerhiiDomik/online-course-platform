from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from course.models import Course

User = get_user_model()


class CourseViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUser',
            password='Password123_'
        )
        self.other_user = User.objects.create_user(
            username='OtherUser',
            password='Password123_'
        )
        self.course = Course.objects.create(
            name="Test Course",
            description="Test Description",
            created_by=self.user
        )

    def test_course_list_view(self):
        self.client.login(username='TestUser', password='Password123_')
        response = self.client.get(reverse('course:course-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/course_list.html')
        self.assertIn(self.course, response.context['courses'])

    def test_course_list_view_not_authenticated(self):
        response = self.client.get(reverse('course:course-list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_course_detail_view(self):
        self.client.login(username='TestUser', password='Password123_')
        response = self.client.get(reverse('course:course-detail', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'course/course_detail.html')
        self.assertEqual(response.context['course'], self.course)

    def test_course_detail_view_not_authenticated(self):
        response = self.client.get(reverse('course:course-detail', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 302)

    def test_course_create_view(self):
        self.client.login(username='TestUser', password='Password123_')
        form_data = {
            'name': 'New Course',
            'description': 'New Course Description',
        }
        response = self.client.post(reverse('course:course-create'), data=form_data)
        self.assertEqual(response.status_code, 302)
        new_course = Course.objects.get(name=form_data['name'])
        self.assertEqual(new_course.created_by, self.user)

    def test_course_create_view_not_authenticated(self):
        form_data = {
            'name': 'New Course',
            'description': 'New Course Description',
        }
        response = self.client.post(reverse('course:course-create'), data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_course_update_view(self):
        self.client.login(username='TestUser', password='Password123_')
        form_data = {
            'name': 'Updated Course',
            'description': 'Updated Course Description',
        }
        response = self.client.post(reverse('course:course-update', kwargs={'course_pk': self.course.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, form_data['name'])

    def test_course_update_view_not_authenticated(self):
        form_data = {
            'name': 'Updated Course',
            'description': 'Updated Course Description',
        }
        response = self.client.post(reverse('course:course-update', kwargs={'course_pk': self.course.pk}), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_course_delete_view(self):
        self.client.login(username='TestUser', password='Password123_')
        response = self.client.post(reverse('course:course-delete', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Course.DoesNotExist):
            Course.objects.get(pk=self.course.pk)

    def test_course_delete_view_not_authenticated(self):
        response = self.client.post(reverse('course:course-delete', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 302)

    def test_only_creator_can_update_course(self):
        self.client.login(username='OtherUser', password='Password123_')
        form_data = {
            'name': 'Unauthorized Update',
            'description': 'This update should not be allowed.',
        }
        response = self.client.post(reverse('course:course-update', kwargs={'course_pk': self.course.pk}),
                                    data=form_data)
        self.assertEqual(response.status_code, 403)  # Ensure forbidden status code
        self.course.refresh_from_db()
        self.assertNotEqual(self.course.name, form_data['name'])  # Ensure the update didn't happen

    def test_only_creator_can_delete_course(self):
        self.client.login(username='OtherUser', password='Password123_')
        response = self.client.post(reverse('course:course-delete', kwargs={'course_pk': self.course.pk}))
        self.assertEqual(response.status_code, 403)  # Ensure forbidden status code
        self.assertTrue(Course.objects.filter(pk=self.course.pk).exists())  # Ensure the course was not deleted

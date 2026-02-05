from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

class TaskSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin = User.objects.create_superuser(username='admin', password='password123')
        
        self.task = Task.objects.create(
            title='Test Task',
            assigned_by=self.admin,
            status='TODO',
            priority=2,
        )
        self.task.assigned_to.add(self.user)

    def test_login_required(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_user_dashboard_only_assigned_tasks(self):
        self.client.login(username='testuser', password='password123')
        # Create another task for another user
        other_user = User.objects.create_user(username='other', password='password123')
        other_task = Task.objects.create(title='Other Task', assigned_by=self.admin)
        other_task.assigned_to.add(other_user)
        
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        self.assertNotContains(response, 'Other Task')

    def test_user_cannot_access_admin_urls(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('admin_task_list'))
        self.assertEqual(response.status_code, 302) # Redirect to login or forbidden

    def test_admin_can_access_all_tasks(self):
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('admin_task_list'))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_access(self):
        # User can see their own task
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('task_detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

        # User cannot see others task
        other_user = User.objects.create_user(username='other2', password='password123')
        other_task = Task.objects.create(title='Other Task 2', assigned_by=self.admin)
        other_task.assigned_to.add(other_user)
        response = self.client.get(reverse('task_detail', args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)

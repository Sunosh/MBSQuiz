from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import QuizProfile

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='secret')
        self.quizprofile = QuizProfile.objects.create(
            user=self.user, total_score=0)

    def test_profile_view(self):
        self.client.login(username='testuser', password='secret')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/user_profile.html')
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.quizprofile.email)
        self.assertContains(response, 'Количество попыток:')
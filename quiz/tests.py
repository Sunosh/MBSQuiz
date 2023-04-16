from django.test import TestCase, Client
from django.urls import reverse
from mixer.backend.django import mixer
from .models import QuizProfile, Subjects, Question, Choice, AttemptedQuestion

class TestPlayView(TestCase):
    def setUp(self):
        self.client = Client()
        self.subject = mixer.blend(Subjects)
        self.question = mixer.blend(Question, subject=self.subject)
        self.choice = mixer.blend(Choice, question=self.question)
        self.quiz_profile = mixer.blend(QuizProfile)

    def test_get_tour_question_with_remaining_questions(self):
        remaining_question = mixer.blend(Question, subject=self.subject, tour=1)
        view = PlayView()
        question = view.get_tour_question(self.quiz_profile)
        self.assertEqual(question, remaining_question)

    def test_get_tour_question_without_remaining_questions(self):
        used_question = mixer.blend(Question, subject=self.subject, tour=1)
        mixer.blend(AttemptedQuestion, quiz_profile=self.quiz_profile, question=used_question)
        view = PlayView()
        question = view.get_tour_question(self.quiz_profile)
        self.assertEqual(question, None)

    def test_get_with_valid_subject_id(self):
        response = self.client.get(reverse('play', args=[self.subject.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/play.html')
        self.assertEqual(response.context.get('subject'), self.subject)

    def test_get_with_invalid_subject_id(self):
        response = self.client.get(reverse('play', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_with_remaining_question(self):
        response = self.client.get(reverse('play', args=[self.subject.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/play.html')
        self.assertTrue(response.context.get('question'))

    def test_get_without_remaining_question(self):
        quiz_profile = mixer.blend(QuizProfile)
        mixer.blend(AttemptedQuestion, quiz_profile=quiz_profile)
        response = self.client.get(reverse('play', args=[self.subject.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/play.html')
        self.assertFalse(response.context.get('question'))

    def test_post_play_again(self):
        attempted_question = mixer.blend(AttemptedQuestion, quiz_profile=self.quiz_profile)
        response = self.client.post(reverse('play'), {'play_again': '1'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(AttemptedQuestion.objects.filter(pk=attempted_question.pk).exists())

    def test_post_with_valid_data(self):
        attempted_question = mixer.blend(AttemptedQuestion, quiz_profile=self.quiz_profile, question=self.question)
        response = self.client.post(reverse('play'), {'question_pk': self.question.pk, 'choice_pk': self.choice.pk})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('attempted_question', args=[attempted_question.pk]))

    def test_post_with_invalid_data(self):
        response = self.client.post(reverse('play'), {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('play'))
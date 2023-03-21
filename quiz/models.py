import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel


class Question(TimeStampedModel):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1

    html = models.TextField(_('Question Text'))
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.html

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')



class Choice(TimeStampedModel):
    MAX_CHOICES_COUNT = 4

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)
    html = models.TextField(_('Choice Text'))

    def __str__(self):
        return self.html

    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответа')



class QuizProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.DecimalField(_('Общий счет'), default=0, decimal_places=2, max_digits=610)

    def __str__(self):
        return f'<QuizProfile: user={self.user}>'

    def get_new_question(self):
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=self).values_list('question__pk', flat=True)
        remaining_questions = Question.objects.exclude(pk__in=used_questions_pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)

    def create_attempt(self, question):
        attempted_question = AttemptedQuestion(question=question, quiz_profile=self)
        attempted_question.save()

    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()

    def update_score(self):
        marks_sum = self.attempts.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score = marks_sum or 0
        self.save()

    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')


class AttemptedQuestion(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(QuizProfile, on_delete=models.CASCADE, related_name='attempts')
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'




class Subjects(TimeStampedModel):
    title = models.CharField(_('Название предмета'), max_length=100)
    questions = models.ManyToManyField(Question, related_name='subjects')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Предмет')
        verbose_name_plural = _('Предметы')


class Grade(TimeStampedModel):
    num = models.PositiveSmallIntegerField(_('Номер класса'), default=5)
    subject = models.ManyToManyField(Subjects, related_name='grades')

    def __str__(self):
        return self.num

    class Meta:
        verbose_name = _(' Номер класса')
        verbose_name_plural = _('Номера Классов')
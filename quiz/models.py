import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from model_utils.models import TimeStampedModel

#  создание непосредственно вопроса...
class Question(TimeStampedModel):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1 # количество вариантов ответов для вопроса

    html = models.TextField(_('Question Text'))  # поле ввода вопроса
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False) # поле возможности публикации
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6) # максимальное количество оценок
    tour = models.PositiveSmallIntegerField(_('Tour'), default=1) # номер тура
    image = models.ImageField(_('Image'), default=None, upload_to='questions/') # изображение к вопросу

    def __str__(self):
        return self.html

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


# ...и непосредственно ответы
class Choice(TimeStampedModel):
    MAX_CHOICES_COUNT = 4 # максимальное количество вариантов ответов на вопрос

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE) # отношение один ко многим к вопросам
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False) # правильный ли ответ
    html = models.TextField(_('Choice Text')) # ввод текста ответа

    def __str__(self):
        return self.html

    class Meta:
        verbose_name = _('Вариант ответа')
        verbose_name_plural = _('Варианты ответа')


   #профиль и счёт для него
class QuizProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #  отношение один к одному к пользователю
    total_score = models.DecimalField(_('Общий счет'), default=0, decimal_places=2, max_digits=610) # общий счет пользователя

    def __str__(self):
        return f'<QuizProfile: user={self.user}>'


    class Meta:
        verbose_name = _('Профиль')
        verbose_name_plural = _('Профили')

    # получение нового варианта ответа
    def create_attempt(self, question):
        attempted_question = AttemptedQuestion(question=question, quiz_profile=self)
        attempted_question.save()

    # сравнение правильного ответа и варианта ответа
    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()

    # обновление счета профиля
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



# предмет, объединяющий вопросы
class Subjects(models.Model):
    title = models.CharField(_('Название предмета'), max_length=100)
    questions = models.ManyToManyField(Question, related_name='subjects')
    grade = models.PositiveSmallIntegerField(_('Номер класса'), default=5)
    def __str__(self):
        return self.title

    def get_grade(self):
        return self.grade

    class Meta:
        verbose_name = _('Предмет')
        verbose_name_plural = _('Предметы')



# класс , объединяющий вопросы
# class Grade(models.Model):
#     num = models.PositiveSmallIntegerField(_('Номер класса'), default=5)
#     subject = models.TextField(_('Предмет'))
#
#     # def __str__(self):
#         return self.num
#
#     class Meta:
#         verbose_name = _(' Номер класса')
#         verbose_name_plural = _('Номера Классов')
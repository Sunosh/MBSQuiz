from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from django.urls import reverse
from .models import QuizProfile, Question, QuestionTour3, AttemptedQuestion, AttemptedQuestionTour3, Subjects
from .forms import UserLoginForm, RegistrationForm
import random


class Play(View):
    template_name = 'quiz/play.html'

    def get_tour_question(self, quiz_profile, subject):
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=quiz_profile, subjects=subject).values_list(
            'question__pk', flat=True)
        used_questions_pk_test = AttemptedQuestion.objects.filter(quiz_profile=quiz_profile, subjects=subject).values_list(
            ('question__pk' and 'subjects'), flat=True)
        remaining_questions_tour1 = Question.objects.exclude(pk__in=used_questions_pk).filter(tour=1)
        if remaining_questions_tour1.exists():
            return random.choice(remaining_questions_tour1)
        else:
            remaining_questions_tour2 = Question.objects.exclude(pk__in=used_questions_pk).filter(tour=2)
            if remaining_questions_tour2.exists():
                return random.choice(remaining_questions_tour2)
            else:
                return None

    def get(self, request, subject_id, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
        subject = Subjects.objects.get(id=subject_id)
        question_X = self.get_tour_question(quiz_profile, subject)
        print(question_X)
        if question_X is not None:
            quiz_profile.create_attempt(question_X, subject)

        context = {
            'subject': subject,
            'question': question_X,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, subject_id, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
        question_pk = request.POST.get('question_pk')
        choice_pk = request.POST.get('choice_pk')
        if not (question_pk and choice_pk):
            return redirect(reverse('quiz:play', args=[subject_id]))

        try:
            attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=int(question_pk))
            selected_choice = attempted_question.question.choices.get(pk=int(choice_pk))
        except (ObjectDoesNotExist, ValueError):
            return redirect(reverse('quiz:play', args=[subject_id]))

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)
        return redirect(reverse('quiz:play', args=[subject_id]))


class PlayTour3(View):
    template_name = 'quiz/playtour3.html'

    def get_tour3_question(self, quiz_profile, subject):
        used_questions_pk = AttemptedQuestionTour3.objects.filter(quiz_profile=quiz_profile, subjects=subject).values_list(
            'question__pk', flat=True)
        remaining_questions_tour3 = QuestionTour3.objects.exclude(pk__in=used_questions_pk)
        if remaining_questions_tour3.exists():
            return random.choice(remaining_questions_tour3)

    def get(self, request, subject_id, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
        subject = Subjects.objects.get(id=subject_id)
        question_XI = self.get_tour3_question(quiz_profile, subject)
        if question_XI is not None:
            quiz_profile.create_attempt3(question_XI, subject)

        context = {
            'subject': subject,
            'question': question_XI,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, subject_id, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
        question_pk = request.POST.get('question_pk')
        text_answer = request.POST.get('text_answer')
        right_answer = QuestionTour3.objects.filter(pk=question_pk).values_list(
            'right_anwser', flat=True).first()
        play_again = request.POST.get('play_again')

        if play_again:
            AttemptedQuestion.objects.filter(quiz_profile=quiz_profile).delete()
            AttemptedQuestionTour3.objects.filter(quiz_profile=quiz_profile).delete()
            return redirect(reverse('quiz:play', args=[subject_id]))
        else:
            if not (question_pk and text_answer):
                return redirect(reverse('quiz:play', args=[subject_id]))

            attempted_question = quiz_profile.attempts3tour.select_related('question').filter(question__pk=int(question_pk)).first()
            
            return redirect(reverse('quiz:play', args=[subject_id]))

    
    

# первейшая(которая открывается при первом запуске) страница
def home(request):
    context = {}
    return render(request, 'quiz/home.html', context=context)


# домашняя страница
@login_required()
def user_home(request):
    context = {}
    return render(request, 'quiz/user_home.html', context=context)

# таблица лидеров
def leaderboard(request):
    top_quiz_profiles = QuizProfile.objects.order_by('-total_score')
    total_count = top_quiz_profiles.count()
    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quiz/leaderboard.html', context=context)

@login_required()
def profile(request):
    quizprofile = QuizProfile.objects.get(user=request.user)
    total_score = quizprofile.total_score

    context = {"quizprofile": quizprofile, "total_score": total_score}
    return render(request, 'quiz/user_profile.html', context=context)


# вход в учётную запись
def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/user-home')
    return render(request, 'quiz/login.html', {"form": form, "title": title})

# создание нового пользователя
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = QuizProfile(user=user) #, grade=form.cleaned_data['grade'])
            profile.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'quiz/registration.html', context=context)

# выход из учётной записи
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required()
def subjects(request):
    subject_order_grade = Subjects.objects.filter(grade__range=(1, 11)).order_by('grade')
    context = {
        'subjects': subject_order_grade,
    }
    return render(request, 'quiz/subjects.html', context=context)


# ошибка 404
def error_404(request):
    data = {}
    return render(request, 'quiz/error_404.html', data)

# ошибка 500
def error_500(request):
    data = {}
    return render(request, 'quiz/error_500.html', data)



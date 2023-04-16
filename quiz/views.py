from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views import View
from django.urls import reverse
from django.views.generic import ListView
from django.db.models import Sum
from django.utils.decorators import method_decorator
from .models import QuizProfile, Question, AttemptedQuestion, Subjects
from .forms import UserLoginForm, RegistrationForm
import random


class Play(View):
    template_name = 'quiz/play.html'

    def get_tour_question(self, quiz_profile):
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=quiz_profile).values_list(
            'question__pk', flat=True)

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
        subject = get_object_or_404(Subjects, id=subject_id)
        subject_list = Subjects.objects.filter(id=subject_id)

        question = self.get_tour_question(quiz_profile)

        if question is not None:
            quiz_profile.create_attempt(question, subject_id)



        context = {
            'subject': subject,
            'questions': question,
            'subject_list': subject_list,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, subject_id, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

        subject_id = get_object_or_404(Subjects, id=subject_id)
        question_pk = request.POST.get('question_pk')
        choice_pk = request.POST.get('choice_pk')
        play_again = request.POST.get('play_again')

        if play_again:
            AttemptedQuestion.objects.filter(quiz_profile=quiz_profile, subjects=int(subject_id)).delete()
            return redirect(reverse('play'))
        else:
            if not (question_pk and choice_pk):
                return redirect(reverse('play'))

            try:
                attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=int(question_pk))
                selected_choice = attempted_question.question.choices.get(pk=int(choice_pk))
            except (ObjectDoesNotExist, ValueError):
                return redirect(reverse('play'))

            quiz_profile.evaluate_attempt(attempted_question, selected_choice)
            return redirect(attempted_question)



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

    top_quiz_profiles = QuizProfile.objects.order_by('-total_score')[:500]
    total_count = top_quiz_profiles.count()
    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quiz/leaderboard.html', context=context)



# промежуточная страница между вопросами
@login_required()
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'quiz/submission_result.html', context=context)

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
            profile = QuizProfile(user=user, grade=form.cleaned_data['grade'])
            profile.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form}

    return render(request, 'registration.html', context=context)

# выход из учётной записи
def logout_view(request):
    logout(request)
    return redirect('/')

# ошибка 404
def error_404(request):
    data = {}
    return render(request, 'quiz/error_404.html', data)

# ошибка 500
def error_500(request):
    data = {}
    return render(request, 'quiz/error_500.html', data)

def subjects(request):
    subject_order_grade = Subjects.objects.filter(grade__range=(1, 11)).order_by('grade')
    context = {
        'subjects': subject_order_grade,
    }
    return render(request, 'quiz/subjects.html', context=context)

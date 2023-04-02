from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views import View
from django.utils.decorators import method_decorator
from .models import QuizProfile, Question, AttemptedQuestion, Subjects
from .forms import UserLoginForm, RegistrationForm


@method_decorator(login_required, name='dispatch')
class PlayView(View):
    template_name = 'quiz/play.html'

    def get_tour_question(self, quiz_profile):
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=quiz_profile).values_list('question__pk', flat=True)
        remaining_questions_tour1 = Question.objects.exclude(pk__in=used_questions_pk).filter(tour=1)
        if remaining_questions_tour1.exists():
            return choice(remaining_questions_tour1)
        remaining_questions_tour2 = Question.objects.exclude(pk__in=used_questions_pk).filter(tour=2)
        if remaining_questions_tour2.exists():
            return choice(remaining_questions_tour2)

    def get(self, request, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

        question = self.get_tour_question(quiz_profile)

        if question is not None:
            attempted_question = AttemptedQuestion.objects.create(
                quiz_profile=quiz_profile,
                question=question,
            )
        else:
            attempted_question = None

        context = {
            'question': question,
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

        if request.method == 'POST':

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

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

# профиль пользователя, его вопросов и вариантов ответов на них
@login_required()
def play(request):
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)
    # subjects_with_grade_1_to_11 = Subjects.objects.filter(grade__gte=1, grade__lte=11).order_by('grade')
    #
    # subject_tuple = ()
    #
    # for subjects in list(subjects_with_grade_1_to_11.values_list('grade', flat=True)):
    #     subject_tuple.append(subjects)
    # list(set(subject_tuple))


    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        if choice_pk is not None:
            try:
                selected_choice = attempted_question.question.choices.get(pk=choice_pk)
            except ObjectDoesNotExist:
                raise Http404

            quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_tour_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'quiz/play.html', context=context)

# промежуточная страница между вопросами
@login_required()
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'quiz/submission_result.html', context=context)

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
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'quiz/registration.html', context=context)

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

def subjects_view(request):
    subjects_with_grade_1_to_11 = Subjects.objects.filter(grade__gte=1, grade__lte=11).order_by('grade')
    context = {'subjects': subjects_with_grade_1_to_11}
    return render(request, 'quiz/subjects.html', context=context)
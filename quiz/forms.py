from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from .models import Question, Choice, Subjects


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['html', 'is_published']
        widgets = {
            'html': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['html', 'is_correct']
        widgets = {
            'html': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
        }


class ChoiceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ChoiceInlineFormset, self).clean()

        correct_choices_count = 0
        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and form.cleaned_data.get('is_correct') is True:
                correct_choices_count += 1

        try:
            assert correct_choices_count == Question.ALLOWED_NUMBER_OF_CORRECT_CHOICES
        except AssertionError:
            raise forms.ValidationError(_('Exactly one correct choice is allowed.'))


User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Пользователь не найден")
            if not user.check_password(password):
                raise forms.ValidationError("Неправильный Пароль")
            if not user.is_active:
                raise forms.ValidationError("Данный пользователь не активен")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    grade = forms.IntegerField(
        required=True,
        label="Класс",
        validators=[
            MinValueValidator(1, "Grade should be between 1 and 11."),
            MaxValueValidator(11, "Grade should be between 1 and 11.")
        ]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'grade',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.grade = self.cleaned_data['grade']

        if commit:
            user.save()

        return user

class QuizRequestForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subjects.objects.filter(grade__range=(1, 11)).order_by('grade'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label=None
    )
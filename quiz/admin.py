from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms.utils import flatatt
from django.forms import widgets
from django.utils.html import format_html
from .models import Question, QuestionTour3, Choice, Subjects, QuizProfile, AttemptedQuestion
from .forms import QuestionForm, ChoiceForm


class ChoiceInline(admin.StackedInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    show_change_link = True
    formset = BaseInlineFormSet
    form = ChoiceForm
    readonly_fields = []

    def formfield_for_dbfield(self, db_field, **kwargs):
        """
        Overrides base method to exclude the checkbox input for each form field.
        """
        if db_field.name == 'is_correct':
            kwargs['widget'] = widgets.HiddenInput()
        return super().formfield_for_dbfield(db_field, **kwargs)

    def get_fieldsets(self, request, obj=None):
        """
        Returns the fieldsets for the inline.
        """
        fs = super().get_fieldsets(request, obj)
        fs[0][1]['fields'] = ['html', 'is_correct']
        return fs


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [ChoiceInline]
    list_display = ['html', 'tour', 'is_published']
    list_filter = ['tour', 'is_published']
    search_fields = ['html', 'choices__html']
    fieldsets = [
        (None, {'fields': ['html']}),
        ('Advanced options', {'fields': ['is_published', 'tour'], 'classes': ['collapse']}),
    ]
    form = QuestionForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.pk is not None and obj.is_published is True:
            return False
        return True

class QuestionTour3Admin(admin.ModelAdmin):
    list_display = ('html', 'is_published', 'maximum_marks', 'right_anwser', 'image')
    list_filter = ('is_published',)
    search_fields = ('html', 'right_anwser')
    fieldsets = (
        (None, {
            'fields': ('html', 'is_published')
        }),
        ('Answer details', {
            'fields': ('maximum_marks', 'right_anwser', 'image')
        })
    )

    def has_delete_permission(self, request, obj=None):
        return False


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade')
    search_fields = ('title', 'questions', 'questions_tour3', 'grade')
    fieldsets = (
        (None, {
            'fields': ('title', 'questions', 'questions_tour3', 'grade')
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionTour3, QuestionTour3Admin)
admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(QuizProfile)
admin.site.register(AttemptedQuestion)

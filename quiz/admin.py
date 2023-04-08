from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms.utils import flatatt
from django.forms import widgets
from django.utils.html import format_html
from .models import Question, Choice, Subjects, QuizProfile, AttemptedQuestion
from .forms import QuestionForm, ChoiceForm


class ReadonlyInlineMixin(object):
    """
    Mixin class to make all fields in an inline read-only.
    """

    def get_readonly_fields(self, request, obj=None):
        """
        Returns all fields in readonly mode.
        """
        return [f.name for f in self.opts.fields]


class ChoiceInline(ReadonlyInlineMixin, admin.StackedInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    show_change_link = True
    formset = BaseInlineFormSet
    form = ChoiceForm
    readonly_fields = ['html']

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
        fs[0][1]['fields'] = ['html']
        return fs


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [ChoiceInline]
    list_display = ['html', 'tour', 'is_published']
    list_filter = ['tour', 'is_published']
    search_fields = ['html', 'choices__html']
    fieldsets = [
        (None, {'fields': ['html', 'image']}),
        ('Advanced options', {'fields': ['is_published', 'tour'], 'classes': ['collapse']}),
    ]
    form = QuestionForm

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.pk is not None and obj.is_published is True:
            return False
        return True


admin.site.register(Question, QuestionAdmin)
admin.site.register(Subjects)
admin.site.register(QuizProfile)
admin.site.register(AttemptedQuestion)
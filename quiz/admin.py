from django.contrib import admin
from .models import Question, Choice, Subjects, QuizProfile, AttemptedQuestion
from .forms import QuestionForm, ChoiceForm, ChoiceInlineFormset
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = False
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    form = ChoiceForm
    formset = ChoiceInlineFormset


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline, )
    list_display = ['html', 'tour', 'is_published']
    list_filter = ['tour', 'is_published']
    search_fields = ['html', 'choices__html']
    fields = ('html', 'is_published', 'tour', 'image')
    actions = None
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

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Question, Choice

class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'

# class CreatePollForm(forms.ModelForm):
#
#     class Meta:
#         model = Question
#         fields = ('question_text',)

class CreateChoiceForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateChoiceForm, self).__init__(*args, **kwargs)

        choices = Choice.objects.filter(
            question=self.instance
        )
        for i in range(len(choices) + 1):
            field_name = 'choice_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = choices[i].choice
            except IndexError:
                self.initial[field_name] = ""
            field_name = 'choice_%s' % (i+1,)
            self.fields[field_name] = forms.CharField(required=False)


    def clean(self):
        choices = set()
        i = 0
        field_name = 'choice_%s' % (i,)
        while self.cleaned_data.get(field_name):
            choice = self.cleaned_data[field_name]
            if choice in choices:
                self.add_error(field_name, 'Duplicate')
            else:
                choices.add(choice)
            i += 1
            field_name = 'choice_%s' % (i,)
        self.cleaned_data['choices'] = choices



    def save(self):
        question = self.instance
        question.question_text = self.cleaned_data['question_text']
        question.author = self.request.user
        question.save()
        question.choice_set.all().delete
        for choice in self.cleaned_data['choices']:
            Choice.objects.create(question=question, choice_text=choice)

    def get_choice_fields(self):
        for field_name in self.fields:
            if field_name.startswith('choice_'):
                yield self[field_name]





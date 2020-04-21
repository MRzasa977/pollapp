from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Question, Choice, User
from django.forms.models import modelformset_factory


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username is already in use')
        return username

class CreatePollForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ('question_text',)
class CreateChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text',]
        widgets = {
            'choice_text': forms.TextInput(attrs={ 'class': 'form-control'}),
        }


# class CreateChoiceForm(forms.ModelForm):
#
#     class Meta:
#         model = Choice
#         fields = ('choice_text',)
#
#
#     def __init__(self, *args, **kwargs):
#         self.question = kwargs.pop('question')
#         super(CreateChoiceForm, self).__init__(*args, **kwargs)



    # def __init__(self, *args, **kwargs):
    #     extra_fields = kwargs.pop('extra', 0)
    #     super(CreateChoiceForm, self).__init__(*args, **kwargs)
    #     self.fields['extra_choice_field'].initial = extra_fields
    #
    #     for index in range(len(extra_fields)):
    #         self.fields['extra_field_{index}'.format(index=index)] = forms.CharField()

# ChoiceFormSet = modelformset_factory(Choice, form=CreateChoiceForm, extra=1)

# class ChoiceFormSet(ChoiceFormSet):
#     def __init__(self, *args ,**kwargs):
#         self.question = kwargs.pop('question')
#         super(ChoiceFormSet, self).__init__(*args, **kwargs)
#         for form in self.forms:
#             form.empty_permitted = False
#
#     def _construct_form(self, *args, **kwargs):
#         kwargs['question'] = self.question
#         return super(ChoiceFormSet,self)._construct_form(*args, **kwargs)

# class CreateChoiceForm(forms.ModelForm):
#
#     class Meta:
#         model = Question
#         fields = ['question_text',]
#
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request')
#         super(CreateChoiceForm, self).__init__(*args, **kwargs)
#
#         choices = Choice.objects.filter(
#             question=self.instance
#         )
#         for i in range(len(choices) + 1):
#             field_name = 'choice_%s' % (i,)
#             self.fields[field_name] = forms.CharField(required=False)
#             try:
#                 self.initial[field_name] = choices[i].choice
#             except IndexError:
#                 self.initial[field_name] = ""
#             field_name = 'choice_%s' % (i+1,)
#             self.fields[field_name] = forms.CharField(required=False)
#
#
#     def clean(self):
#         choices = set()
#         i = 0
#         field_name = 'choice_%s' % (i,)
#         while self.cleaned_data.get(field_name):
#             choice = self.cleaned_data[field_name]
#             if choice in choices:
#                 self.add_error(field_name, 'Duplicate')
#             else:
#                 choices.add(choice)
#             i += 1
#             field_name = 'choice_%s' % (i,)
#         self.cleaned_data['choices'] = choices


    #
    # def save(self):
    #     question = self.instance
    #     question.question_text = self.cleaned_data['question_text']
    #     question.author = self.request.user
    #     question.save()
    #     question.choice_set.all().delete
    #     for choice in self.cleaned_data['choices']:
    #         Choice.objects.create(question=question, choice_text=choice)
    #
    # def get_choice_fields(self):
    #     for field_name in self.fields:
    #         if field_name.startswith('choice_'):
    #             yield self[field_name]





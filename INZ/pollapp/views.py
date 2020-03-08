from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateChoiceForm
from.models import Question
from django.utils import timezone

from .models import Choice, Question
from . import forms

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = 'polls/index.html'

class ListView(generic.ListView):
    template_name = 'polls/createdPolls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('id')

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class UserPolls(LoginRequiredMixin,generic.ListView):
    template_name = 'polls/myPolls.html'
    model = Question
    context_object_name = 'user_questions_list'

    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollapp:results', args=(question.id,)))

class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class CreatePoll(LoginRequiredMixin, generic.CreateView):
    form_class = forms.CreateChoiceForm
    template_name = 'polls/createPoll.html'
    success_url = reverse_lazy('pollapp:index')

    # def form_valid(self, form):
    #     self.object = poll = form.save(commit=False)
    #     poll.author = self.request.user
    #     poll.save()
    #     return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CreatePoll, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.request = self.request
        return form

    def get_success_url(self):
        return reverse('pollapp:userPolls')
        # return reverse('pollapp:index')
# class CreateChoicePoll(LoginRequiredMixin, generic.CreateView):
#     form_class = forms.CreateChoiceForm
#     model = Choice
#     template_name = 'polls/createChoice.html'
#     success_url = reverse_lazy('pollapp:index')
#     # def get(self, request, *args, **kwargs):
#     #     form = CreatePollForm()
#     #     return render(request, self.template_name, {'form':form})
#     # def post(self, request, *args, **kwargs):
#     #     form = CreateChoiceForm(request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         form.choice_text = form.cleaned_data['choice_text']
#     #         form = CreateChoiceForm()
#     #         return redirect('pollapp:index')
#     #     args = {'form': form}
#     #     return render(request, self.template_name, args)
#     def form_valid(self, form):
#         post = get_object_or_404(Question, pk=pk)
#         choice = form.save(commit=False)
#         choice.question = post
#         choice.save()
#         return super().form_valid(form)

def createChoice(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method =='POST':
        form = CreateChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('pollapp:detail', pk=question.pk)
    else:
        form = CreateChoiceForm()
    return render(request, 'polls/createChoice.html', {'form': form})




from django.db import models
from django.utils import timezone
import datetime
from django.contrib import auth
from django.db.models import Sum
# Create your models here.

User = auth.get_user_model()

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    def __str__(self):
        return self.question_text
    def total_votes(self):
        """Calculates the total number of votes for this poll."""
        return self.choice_set.aggregate(Sum('votes'))['votes__sum']

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    def get_votes_perc(self):
        """Calculates the percentage of votes for this choice."""
        total = self.question.total_votes()
        return self.votes / float(total) * 100 if total > 0 else 0


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)

class Votes_ip(models.Model):
    client_ip = models.GenericIPAddressField()
    voted_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.client_ip
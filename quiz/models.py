from django.db import models
from django.contrib.auth.models import User
from users.models import Profile
from django.utils import timezone


class Quiz(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class QuizAttempt(models.Model):
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_attempts = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quiz} attempt {self.no_of_attempts} by {self.user}'


class Question(models.Model):
    que = models.CharField(max_length=200)
    A = models.CharField(max_length=200)
    B = models.CharField(max_length=200)
    C = models.CharField(max_length=200)
    D = models.CharField(max_length=200)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answer_choices = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    ans = models.CharField(max_length=1, choices=answer_choices)

    def __str__(self):
        return self.que


class Attempt(models.Model):
    is_attempted = models.BooleanField(default=True)
    chosen = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='NA')
    que = models.ForeignKey(Question, on_delete=models.CASCADE)
    attempted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    attempt_no = models.IntegerField(default=0)

    def __str__(self):
        return self.chosen


def question_options_list(quiz):
    questions_list = Question.objects.filter(quiz=quiz)
    options_list = []
    for question in questions_list:
        joint_options = ''
        for key, value in question.answer_choices:
            joint_options = joint_options + key + ':' + getattr(question, key) + '<br>'
        options_list.append(joint_options)
    return list(map(lambda u, v: u.que + '<br>' + v, questions_list, options_list))
    #adds two strings, the question statement and the joint options string





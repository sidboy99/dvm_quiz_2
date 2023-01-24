from django.contrib import admin
from .models import Quiz, Question, Attempt, QuizAttempt

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Attempt)
admin.site.register(QuizAttempt)
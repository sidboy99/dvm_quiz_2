from django.urls import path
from quiz import views as quiz_views

urlpatterns = [
    path('quiz/attempt/<int:pk>/', quiz_views.show_question_form, name='quiz-attempt'),
    path('quiz/create/', quiz_views.create_quiz_form, name='quiz-create'),
    path('', quiz_views.QuizListView.as_view(), name='home'),
    path('quiz/create/<int:quiz_pk>/<int:question_no>', quiz_views.create_question_form, name='question-create'),
    path('quiz/view-attempts/', quiz_views.show_user_attempts, name='quiz-user-attempts'),
    path('quiz/view-attempts/<int:quiz_pk>', quiz_views.show_user_quiz_attempt, name='quiz-user-curr-attempt'),
    path('quiz/delete-question/<int:question_pk>/<int:quiz_pk>/<int:question_no>/', quiz_views.delete_question, name='question-delete'),
    path('quiz/delete-quiz/<int:quiz_pk>', quiz_views.delete_quiz, name='quiz-delete')
]
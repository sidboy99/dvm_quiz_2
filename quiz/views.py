from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Quiz, QuizAttempt, Question, Attempt, question_options_list
from .forms import QuizTakerForm, QuestionMakerForm, QuizMakerForm
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseForbidden
from django.forms import formset_factory


@login_required
def show_question_form(request, pk):
    if request.user.profile.user_type == 'QT':
        quiz = Quiz.objects.get(pk=pk)
        if len(QuizAttempt.objects.filter(quiz=quiz, user=request.user)) == 0:
            quiz_attempt = QuizAttempt()
            quiz_attempt.quiz = quiz
            quiz_attempt.user = request.user
            quiz_attempt.save()
        else:
            quiz_attempt = QuizAttempt.objects.filter(quiz=quiz, user=request.user).last()

        questions_list = Question.objects.filter(quiz=quiz)
        q_a_list = question_options_list(quiz)
        QuizFormSet = formset_factory(QuizTakerForm, extra=len(questions_list))

        if request.method =='POST':
            formset = QuizFormSet(request.POST)
            if formset.is_valid():
                current_attempt = quiz_attempt.no_of_attempts + 1
                i = 0
                for dict_ in formset.cleaned_data:
                    if len(dict_) != 0:
                        loc = i
                        attempt = Attempt.objects.create(chosen=dict_['chosen'], que=questions_list[loc],
                                                         attempted_by=request.user, quiz=quiz_attempt, attempt_no=current_attempt)
                        attempt.save()
                        i += 1
                    else:
                        loc = i
                        attempt = Attempt.objects.create(que=questions_list[loc],
                                                         attempted_by=request.user, quiz=quiz_attempt,
                                                         attempt_no=current_attempt)
                        attempt.is_attempted = False


                quiz_attempt.score = 0
                for attempt in Attempt.objects.filter(quiz=quiz_attempt):
                    if (attempt.chosen == attempt.que.ans) and (attempt.attempt_no == current_attempt) and attempt.is_attempted:
                        quiz_attempt.score += 1
                quiz_attempt.no_of_attempts += 1
                quiz.save()
                quiz_attempt.save()
                return redirect('quiz-user-curr-attempt', quiz.pk)

        formset = QuizFormSet()
        zipped_list = list(zip(q_a_list, formset))

        return render(request, 'quiz/quiz_form.html', {'zipped_list':zipped_list, 'formset':formset, 'quiz':quiz})
    else:
        return HttpResponseForbidden('You must be a QT to access this page.')


class QuizListView(ListView):
    model = Quiz
    template_name = 'quiz/home.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            if self.request.user.profile.user_type == 'QM':
                return queryset.filter(author=self.request.user)
            else:
                return queryset
        except AttributeError:
            return None


@login_required
def create_quiz_form(request):
    if request.user.profile.user_type == 'QM':
        if request.method == 'POST':
            form = QuizMakerForm(request.POST)
            form.instance.author = request.user
            if form.is_valid():
                form.save()
                quiz_pk = Quiz.objects.filter(author=request.user).last().pk
                return redirect('question-create', quiz_pk, 1)
        else:
            form = QuizMakerForm()

        return render(request, 'quiz/quiz_create.html', {'form': form})
    else:
        return HttpResponseForbidden('You must be a QM to access this page')


@login_required
def create_question_form(request, quiz_pk, question_no):
    if request.user.profile.user_type == 'QM':
        quiz = Quiz.objects.filter(pk=quiz_pk, author=request.user).last()
        can_access_next = True
        question = Question()
        question_list = list(Question.objects.filter(quiz=quiz))
        if request.method == 'POST':
            if 1 <= question_no <= len(question_list): # for updating a question
                question = question_list[question_no-1]
                question.delete()
                form = QuestionMakerForm(request.POST)
                form.instance.quiz = quiz
                if form.is_valid():
                    form.save()
                    return redirect('question-create', quiz_pk, question_no+1)
            else:
                form = QuestionMakerForm(request.POST)
                form.instance.quiz = quiz
                if form.is_valid():
                    form.save()
                    return redirect('question-create', quiz_pk, question_no + 1)

        else:
            if 1 <= question_no <= len(question_list):
                question = question_list[question_no - 1]
                form = QuestionMakerForm(instance=question)
            elif question_no == len(question_list)+1:
                form = QuestionMakerForm()
                can_access_next = False
            else:
                raise Http404('Error: Question number out of bounds.')


        context = {
            'form': form,
            'quiz_pk': quiz_pk,
            'question_no': question_no,
            'can_access_next': can_access_next,
            'question': question
        }
        return render(request, 'quiz/question_create.html', context)
    else:
        return HttpResponseForbidden('You must be a QM to access this page.')


@login_required
def show_user_attempts(request):
    if request.user.profile.user_type == 'QT':
        quizzes_attempted_list = list(QuizAttempt.objects.filter(user=request.user))
        return render(request, 'quiz/view_attempts.html', {'quiz_attempts': quizzes_attempted_list})
    else:
        return HttpResponseForbidden('You must be a QT to access this page')


@login_required
def show_user_quiz_attempt(request, quiz_pk):
    if request.user.profile.user_type == 'QT':
        quiz = Quiz.objects.get(pk=quiz_pk)
        quiz_attempt = QuizAttempt.objects.get(user=request.user, quiz=quiz)
        attempts = Attempt.objects.filter(quiz=quiz_attempt, attempt_no=quiz_attempt.no_of_attempts)

        context = {
            'quiz': quiz,
            'quiz_attempt': quiz_attempt,
            'attempts': attempts,
        }

        return render(request, 'quiz/view_quiz_attempt.html', context)
    else:
        return HttpResponseForbidden('You must be a QT to access this page.')


@login_required
def delete_question(request, question_pk, quiz_pk, question_no):
    if request.user.profile.user_type == 'QM':
        if Quiz.objects.get(pk=quiz_pk).author == request.user:
            question = Question.objects.get(pk=question_pk)
            question.delete()
            return redirect('question-create', quiz_pk, question_no)
        else:
            return redirect('home')
    else:
        return HttpResponseForbidden('You must be a QM to access this page.')


@login_required
def delete_quiz(request, quiz_pk):
    if request.user.profile.user_type == 'QM':
        if Quiz.objects.get(pk=quiz_pk).author == request.user:
            quiz = Quiz.objects.get(pk=quiz_pk)
            quiz.delete()
            return redirect('home')
        else:
            return HttpResponseForbidden('Dude, I ain\'t leaving a security hole here.')
    else:
        return HttpResponseForbidden('You must be a QM to access this page')





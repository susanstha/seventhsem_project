from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Q
from hitcount.views import HitCountDetailView

from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from django.views import generic

from questions.forms import AnswerForm
from .models import Question, Answer
from django.contrib.auth.decorators import login_required

from braces.views import SelectRelatedMixin

# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import pandas as pd

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class QuestionList(SelectRelatedMixin, generic.ListView):
    model = models.Question
    select_related = ("user", "group")


class UserQuestions(generic.ListView):
    model = models.Question
    template_name = "questions/user_question_list.html"

    def get_queryset(self):
        try:
            self.question_user = User.objects.prefetch_related("questions").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.question_user.questions.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_user"] = self.question_user
        return context


class QuestionDetail(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    model = models.Question
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

class QuestionCountHitDetailView(QuestionDetail, HitCountDetailView):
    """
        Generic hitcount class based view that will also perform the hitcount logic.
    """
    count_hit = True


def search(request):
    questions = Question.objects.all()
    query = request.GET.get("q")
    if query:
        questions = questions.filter(
            Q(question__icontains=query)
        ).distinct()
        return render(request, 'questions/question_list.html', {
            'question_list': questions,
        })
    else:
        return render(request, 'questions/question_list.html', {'question_list': questions})


class CreateQuestion(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('question','group')
    model = models.Question

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({"user": self.request.user})
    #     return kwargs

    # def cosine_similarity(self, a, b):
    #     question_from_user =
    #     database_question = Question.objects.all()
    #
    #     documents = [database_question, question_from_user]
    #
    #     count_vectorizer = CountVectorizer(stop_words='english')
    #     count_vectorizer = CountVectorizer()
    #     sparse_matrix = count_vectorizer.fit_transform(documents)
    #
    #     doc_term_matrix = sparse_matrix.todense()
    #     df = pd.DataFrame(doc_term_matrix,
    #                       columns=count_vectorizer.get_feature_names(),
    #                       index=[database_question, question_from_user])
    #     result = (cosine_similarity(df, df))
    #     result = result[0, 1]
    #     if (result > 0.8):
    #         return  redirect('questions:single')
    #     else:
    #         return

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeleteQuestion(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Question
    select_related = ("user", "group")
    success_url = reverse_lazy("questions:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Question Deleted")
        return super().delete(*args, **kwargs)

@login_required
def add_answer_to_question(request, username, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('questions:single', username= question.user.username, pk=question.pk)
    else:
        form = AnswerForm()
        return render(request, 'questions/answer_form.html', {'form': form})


@login_required
def answer_approve(request, username, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.approve()
    return redirect('questions:single',username=username, pk=answer.question.pk)


@login_required
def answer_remove(request, username, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question_pk = answer.question.pk
    answer.delete()
    return redirect('questions:single', username=username, pk=question_pk)

@login_required
def unanswered(request):

    unanswered_questions = Question.objects.filter(answer=None).all()

    context = {
        'unanswered_questions' : unanswered_questions
    }

    return render(request,'questions/unanswered_question.html', context)

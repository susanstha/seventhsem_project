from django.conf.urls import url

from . import views

app_name='questions'

urlpatterns = [
    url(r"^$", views.QuestionList.as_view(), name="all"),
    url(r"unanswered/$", views.unanswered, name="unanswered"),
    url(r"search/$", views.search, name="search"),
    url(r"new/$", views.CreateQuestion.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/$",views.UserQuestions.as_view(),name="for_user"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$", views.QuestionCountHitDetailView.as_view(), name="single"),
    # url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.QuestionDetail.as_view(),name="single"),
    url(r"delete/(?P<pk>\d+)/$",views.DeleteQuestion.as_view(),name="delete"),

    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/answer/$", views.add_answer_to_question, name="add_answer_to_question"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/approve/$", views.answer_approve, name="answer_approve"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/remove/$", views.answer_remove, name="answer_remove"),
]

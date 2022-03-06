from django.urls import include, path

from .views import CreateQuestionView, QuestionDetailView, QuestionListView
from .views import create_answer


app_name = 'questions'    # 指定路由的命名空间


urlpatterns = [
    path('questions/', include(([
        path('', QuestionListView.as_view(), name='questions_list'),
        path('add/', CreateQuestionView.as_view(), name='create_question'),
        path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
        path('<int:pk>/add', create_answer, name='create_answer'),
    ])))
]
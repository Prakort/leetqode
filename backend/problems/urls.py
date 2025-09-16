from django.urls import path
from . import views

urlpatterns = [
    # Core endpoints
    path('problems/', views.ProblemListAPIView.as_view(), name='problem_list'),
    path('user/problems/', views.UserProblemListView.as_view(), name='user_problem_list'),
    path('user/problems/<int:pk>/update/', views.UserProblemUpdateView.as_view(), name='user_problem_update'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stats/', views.problem_stats, name='problem_stats'),
]

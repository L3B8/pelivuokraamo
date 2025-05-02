from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    GameListView, GameDetailView, LoanCreateView,
    LoanHistoryView, return_game, RegisterView
)

urlpatterns = [
    path('', GameListView.as_view(), name="game_list"),
    path('game/<int:pk>/', GameDetailView.as_view(), name="game_detail"),
    path('game/<int:pk>/loan/', LoanCreateView.as_view(), name="loan_game"),
    path('loans/', LoanHistoryView.as_view(), name="loan_history"),
    path('loan/<int:pk>/return/', return_game, name="return_game"),
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="vuokraus/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    
]

from django.urls import path, include
from .views import DeleteView, RegisterView,LoginView,LogoutView,EditView,AllUsersView,UserView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user',UserView.as_view()),
    path('all_users',AllUsersView.as_view()),
    path('logout',LogoutView.as_view()),
    path('edit',EditView.as_view()),
    path('delete',DeleteView.as_view()),
]
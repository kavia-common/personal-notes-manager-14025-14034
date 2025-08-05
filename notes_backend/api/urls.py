from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health, name='Health'),

    # User Authentication
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # CRUD for Notes
    path('notes/', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', views.NoteRetrieveUpdateDestroyView.as_view(), name='note-rud'),
]

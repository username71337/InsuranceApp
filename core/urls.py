from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_choose, name='signup_choose'),
    path('signup/member/', views.member_signup, name='member_signup'),
    path('signup/consultant/', views.consultant_signup, name='consultant_signup'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Consultant
    path('consultant/<int:pk>/', views.consultant_detail, name='consultant_detail'),

    # Consultation
    path('consult/<int:consultant_pk>/', views.consult_request, name='consult_request'),
    path('consultations/', views.my_consultations, name='my_consultations'),
    path('consultations/<int:pk>/status/<str:status>/', views.update_consultation_status, name='update_consultation_status'),

    # Messaging
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
]

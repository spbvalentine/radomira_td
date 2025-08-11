from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_index, name='dashboard_index'),
    path('call/', views.dashboard_call, name='call'),
    path('login/', views.login_view, name='dashboard_login'),
    path('logout/', views.logout_view, name='logout'),
    path('calls/', views.dashboard_calls, name='dashboard_calls'),
    path('reports/', views.dashboard_report, name='dashboard_report'),
    path('calls/<int:call_id>/', views.call_edit, name='call_edit'),
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_root_url, name='login'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('login/common/', views.common_dashboard, name='common_dashboard'),
    path('login/ra/', views.ra_dashboard, name='ra_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),  # A shared dashboard view
    path('anonymous/', views.anonymous_view, name='anonymous_view'),
    path('profile/', views.profile_view, name='profile'),
    path('setting/', views.setting_view, name='setting'),
    path('resources/', views.contact_view, name='resources'),
    path('notification/', views.notification_view, name='notification'),
    path('save-background-color/', views.save_background_color, name='save_background_color'),
]



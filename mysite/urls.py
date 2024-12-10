"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from ra_pma import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_choice, name='login'),
    path('admin/', admin.site.urls),
    path('login/', views.login_choice, name='login'),
    path('set-role-and-login/', views.set_role_and_login, name='set_role_and_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/common/', views.common_dashboard, name='common_dashboard'),
    path('auth/', include('social_django.urls', namespace='social')),  # Google OAuth URLs
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('events/', include('events.urls')),
    path('', include('ra_pma.urls')),  # Include ra_pma app URLs last
]

handler404 = "ra_pma.views.custom_404"
handler403 = "ra_pma.views.custom_403"
handler500 = "ra_pma.views.custom_500"
handler400 = "ra_pma.views.custom_400"

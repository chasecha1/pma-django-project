from django.urls import path
from . import views

urlpatterns = [
    path('add_event/', views.add_event, name='add_event'),
    path('get_calendar_events/<str:year_month>/', views.get_calendar_events, name='get_calendar_events'),
    path('get_events/', views.get_events, name='get_events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('request_to_join/<int:event_id>/', views.request_to_join, name='request_to_join'),
    path('approve_request/<int:event_id>/<int:user_id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:event_id>/<int:user_id>/', views.reject_request, name='reject_request'),
    path('leave-event/<int:event_id>/', views.leave_event, name='leave_event'),

]

from django.urls import path, include
from Darwin import views
urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('announcements/', views.announcements_view, name='announcements'),
    path('leave_request/', views.leave_request_view, name='leave_request'),
    path('upcoming_events/', views.upcoming_events_view, name='upcoming_events'),
    path('create_announcement/', views.create_announcement_view, name='create_announcement'),
    path('publish_attendance/', views.publish_attendance, name='publish_attendance'),
    path('marks_upload/', views.marks_upload, name='marks_upload'),
    path('settings/', views.profile_view, name='settings'),
    path('help/', views.profile_view, name='help'),
    path('articles/', views.profile_view, name='articles'),

    path('studentmarks/', views.marks_view, name='studentmarks'),
    path('attendance/', views.user_attendance_view, name='user_attendance'),
    path('todays_topics/', views.today_topics_view, name='todays_topics'),
    path('athenium/', views.athenium_view, name='athenium'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('explain_marks/', views.explain_marks_view, name='explain_marks'),
    path('feestatus/', views.fee_status_view, name='fee_status')

]

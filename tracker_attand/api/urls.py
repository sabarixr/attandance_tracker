from django.urls import path

from .admin import admin
from .views import *

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('signup/student/', StudentSingUpview.as_view()),
    path('login/', LoginAuthToken.as_view()),
    path('logout/', LogoutView.as_view()),
    path('teacher-only/', TeacherOnlyView.as_view()),
    path('student-only/', StudentOnlyView.as_view()),
    path('courses/', CourseNameListView.as_view()),  
    path('courses/<int:pk>/', CourseNameDetailView.as_view()), 
    path('courses/<int:course_id>/classes/', ClassNameListView.as_view()),  
    path('courses/<int:course_id>/classes/<int:pk>/', ClassNameDetailView.as_view()),  
    path('courses/<int:course_id>/classes/<int:class_id>/hours/', HourListCreateView.as_view()), 
    path('courses/<int:course_id>/classes/<int:class_id>/hours/<int:pk>/', HourListDetailView.as_view()),
    path('courses/<int:course_id>/classes/<int:class_id>/hours/<int:hours_id>/tr-scan', TeacherScanView.as_view()), 
    path('courses/<int:course_id>/classes/<int:class_id>/hours/<int:hours_id>/attendance', AttendanceSessionListView.as_view()),
]

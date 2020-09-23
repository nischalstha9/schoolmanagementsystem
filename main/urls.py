from django.urls import path, include
from .views import home, create_student, StudentListView, create_teacher, StudentUpdateView, TeacherListView, udpate_teacher, UserDeleteView, SessionListView, SessionCreateView, SessionUpdateView, SessionDeleteView, TermCreateView, TermDeleteView, TermUpdateView, TermListView, SubjectListView, SubjectDeleteView, SubjectCreateView, SubjectUpdateView, ClassUpdateView, ClassCreateView, ClassDeleteView, ClassListView, siteconfig_view, current_session_view

app_name = 'main'
urlpatterns = [
    path("", home, name="home"),
    path('site-config/', siteconfig_view, name='configs'),
    path('current-session/', current_session_view, name='current-session'),

    path("new_admission/", create_student, name="new-admission"),
    path("students/", StudentListView.as_view(), name="student-list"),
    path("<int:pk>/student_update/", StudentUpdateView, name="student-update"),

    path("new_teacher/", create_teacher, name="new-teacher"),
    path("teachers/", TeacherListView.as_view(), name="teacher-list"),
    path("<int:pk>/teacher_update/", udpate_teacher, name="teacher-update"),

    path("<int:pk>/user_delete/", UserDeleteView.as_view(), name="user-delete"),

    path("sessions/", SessionListView.as_view(), name="session-list"),
    path("sessions/new/", SessionCreateView.as_view(), name="session-create"),
    path("sessions/<int:pk>/update/", SessionUpdateView.as_view(), name="session-update"),
    path("sessions/<int:pk>/delete/", SessionDeleteView.as_view(), name="session-delete"),

    path('term/list/', TermListView.as_view(), name='terms'),
    path('term/create/', TermCreateView.as_view(), name='term-create'),
    path('term/<int:pk>/update/', TermUpdateView.as_view(), name='term-update'),
    path('term/<int:pk>/delete/', TermDeleteView.as_view(), name='term-delete'),

    path('subject/list/', SubjectListView.as_view(), name='subjects'),
    path('subject/create/', SubjectCreateView.as_view(), name='subject-create'),
    path('subject/<int:pk>/update/', SubjectUpdateView.as_view(), name='subject-update'),
    path('subject/<int:pk>/delete/', SubjectDeleteView.as_view(), name='subject-delete'),

    
    path('class/list/', ClassListView.as_view(), name='classes'),
    path('class/create/', ClassCreateView.as_view(), name='class-create'),
    path('class/<int:pk>/update/', ClassUpdateView.as_view(), name='class-update'),
    path('class/<int:pk>/delete/', ClassDeleteView.as_view(), name='class-delete'),
]
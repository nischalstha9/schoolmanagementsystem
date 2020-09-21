from django.urls import path, include
from .views import home, create_student, StudentListView, create_teacher, StudentUpdateView, TeacherListView, udpate_teacher, UserDeleteView

app_name = 'main'
urlpatterns = [
    path("", home, name="home"),
    path("new_admission/", create_student, name="new-admission"),
    path("<int:pk>/student_update/", StudentUpdateView, name="student-update"),
    path("<int:pk>/user_delete/", UserDeleteView.as_view(), name="user-delete"),
    path("<int:pk>/teacher_update/", udpate_teacher, name="teacher-update"),
    path("new_teacher/", create_teacher, name="new-teacher"),
    path("students/", StudentListView.as_view(), name="student-list"),
    path("teachers/", TeacherListView.as_view(), name="teacher-list"),
]
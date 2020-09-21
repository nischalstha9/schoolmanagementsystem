from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .forms import AdmissionForm1, AdmissionForm2, TeacherProfileForm, TeacherForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from accounts.models import Student, Teacher
from django.views.generic import ListView, DeleteView
from accounts.models import User


# Create your views here.
def home(request):
    return render(request, 'home.html')

def view_404(request, *args, **kwargs):
    return render(request,'partial/404.html',{'title':'Oops! Page Not Found!!'}, status=404)

class StudentListView(ListView):
    model = Student
    template_name = "administration/student_list.html"
    paginate_by = 50
    context_object_name = 'students'

class TeacherListView(ListView):
    model = Teacher
    template_name = "administration/teacher_list.html"
    paginate_by = 50
    context_object_name = 'teachers'


@staff_member_required
def create_student(request, *args, **kwargs):
    context = {}
    context['form1']=AdmissionForm1
    context['form2']=AdmissionForm2
    if request.method=="POST":
        form1 = AdmissionForm1(request.POST)
        semail = f"{request.POST.get('first_name')}.{request.POST.get('last_name')}_{request.POST.get('Class')}{request.POST.get('section')}{request.POST.get('roll')}@student.com"
        pword = make_password("student123@")
        form1.instance.email = semail
        form1.instance.password = pword
        student = form1.save()
        form2 = AdmissionForm2(request.POST)
        form2.instance.user = student
        form2.save()
        messages.success(request, f'Student Admitted Successfully!')
        return redirect('/')
    return render(request, 'administration/create_student.html', context)

@staff_member_required
def create_teacher(request, *args, **kwargs):
    context = {}
    context['form1']=TeacherForm
    context['form2']=TeacherProfileForm
    if request.method=="POST":
        form1 = TeacherForm(request.POST)
        semail = f"{request.POST.get('first_name')}.{request.POST.get('last_name')}_{request.POST.get('contact')}@student.com"
        pword = make_password("teacher123@")
        form1.instance.email = semail
        form1.instance.password = pword
        teacher = form1.save()
        form2 = TeacherProfileForm(request.POST)
        form2.instance.user = teacher
        form2.save()
        messages.success(request, f'Teacher Created Successfully!')
        return redirect('/')
    return render(request, 'administration/create_teacher.html', context)

@staff_member_required
def StudentUpdateView(request, pk, *args, **kwargs):
    stn = Student.objects.get(pk = pk)
    context = {}
    context['form1']=AdmissionForm1(instance = stn)
    context['form2']=AdmissionForm2(instance=stn.profile)
    if request.method=="POST":
        form1 = AdmissionForm1(request.POST, instance = stn)
        form1.save()
        form2 = AdmissionForm2(request.POST, instance=stn.profile)
        form2.save()
        messages.success(request, f'Student Updated Successfully!')
        return redirect('/')
    return render(request, 'administration/create_student.html', context)



@staff_member_required
def udpate_teacher(request, pk, *args, **kwargs):
    tch = Teacher.objects.get(pk = pk)
    context = {}
    context['form1']=TeacherForm(instance=tch)
    context['form2']=TeacherProfileForm(instance=tch.profile)
    if request.method=="POST":
        form1 = TeacherForm(request.POST, instance=tch)
        teacher = form1.save()
        form2 = TeacherProfileForm(request.POST, instance=tch.profile)
        form2.save()
        messages.success(request, f'Teacher Updated Successfully!')
        return redirect('/')
    return render(request, 'administration/create_teacher.html', context)

class UserDeleteView(DeleteView):
    model = User
    template_name = "administration/delete_object.html"
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from accounts.models import Student, Teacher, StudentProfile, Class, Section
from django.views.generic import ListView
from django.views.generic.edit import  DeleteView, CreateView, UpdateView
from accounts.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import AcademicSession, AcademicTerm, Subject, SiteConfig
from .forms import AdmissionForm1, AdmissionForm2, TeacherProfileForm, TeacherForm, AcademicSessionForm, AcademicTermForm, SubjectForm, StudentClassForm, SiteConfigForm, CurrentSessionForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required
def siteconfig_view(request):
  """ Site Config View """
  if request.method == 'POST':
    form = SiteConfigForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Configurations successfully updated')
      return HttpResponseRedirect('site-config')
  else:
    form = SiteConfigForm(queryset=SiteConfig.objects.all())

  context = {"formset": form, "title": "Configuration"}
  return render(request, 'corecode/siteconfig.html', context)

#class
class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
  model = Class
  template_name = 'corecode/class_list.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = StudentClassForm()
      return context

class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
  form_class = StudentClassForm
  template_name = 'corecode/mgt_form.html'
  success_url = reverse_lazy('main:classes')
  success_message = 'New class successfully added'

class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
  model = Class
  fields = ['name']
  success_url = reverse_lazy('main:classes')
  success_message = 'class successfully updated.'
  template_name = 'corecode/mgt_form.html'

class ClassDeleteView(LoginRequiredMixin, DeleteView):
  model = Class
  success_url = reverse_lazy('main:classes')
  template_name = 'corecode/core_confirm_delete.html'
  success_message = "The class {} has been deleted with all its attached content"

  def delete(self, request, *args, **kwargs):
      obj = self.get_object()
      print(obj.name)
      messages.success(self.request, self.success_message.format(obj.name))
      return super(ClassDeleteView, self).delete(request, *args, **kwargs)



#subject

class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
  model = Subject
  template_name = 'corecode/subject_list.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = SubjectForm()
      return context

class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
  form_class = SubjectForm
  template_name = 'corecode/mgt_form.html'
  success_url = reverse_lazy('main:subjects')
  success_message = 'New subject successfully added'

class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
  model = Subject
  fields = ['name']
  success_url = reverse_lazy('main:subjects')
  success_message = 'Subject successfully updated.'
  template_name = 'corecode/mgt_form.html'

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
  model = Subject
  success_url = reverse_lazy('main:subjects')
  template_name = 'corecode/core_confirm_delete.html'
  success_message = "The subject {} has been deleted with all its attached content"

  def delete(self, request, *args, **kwargs):
      obj = self.get_object()
      messages.success(self.request, self.success_message.format(obj.name))
      return super(SubjectDeleteView, self).delete(request, *args, **kwargs)


@login_required
def current_session_view(request):
  """ Current SEssion and Term """
  if request.method == 'POST':
    form = CurrentSessionForm(request.POST)
    if form.is_valid():
      session = form.cleaned_data['current_session']
      term = form.cleaned_data['current_term']
      AcademicSession.objects.filter(name=session).update(current=True)
      AcademicSession.objects.exclude(name=session).update(current=False)
      AcademicTerm.objects.filter(name=term).update(current=True)
      AcademicTerm.objects.exclude(name=term).update(current=False)

  else:
    form = CurrentSessionForm(initial={
      "current_session": AcademicSession.objects.get(current=True),
      "current_term": AcademicTerm.objects.get(current=True)
    })


  return render(request, 'corecode/current_session.html', {"form":form})


#academic terms

class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
  model = AcademicTerm
  template_name = 'corecode/term_list.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = AcademicTermForm()
      return context

class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
  form_class = AcademicTermForm
  template_name = 'corecode/mgt_form.html'
  success_url = reverse_lazy('main:terms')
  success_message = 'New term successfully added'

class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
  form_class = AcademicTermForm
  success_url = reverse_lazy('main:terms')
  success_message = 'Term successfully updated.'
  template_name = 'corecode/mgt_form.html'
  queryset = AcademicTerm.objects.all()

  def form_valid(self, form):
    obj = self.object
    if obj.current == False:
      terms = AcademicTerm.objects.filter(current=True).exclude(name=obj.name).exists()
      if not terms:
        messages.warning(self.request, 'You must set a term to current.')
        return redirect('term')
    return super().form_valid(form)

class TermDeleteView(LoginRequiredMixin, DeleteView):
  model = AcademicTerm
  success_url = reverse_lazy('main:terms')
  template_name = 'corecode/core_confirm_delete.html'
  success_message = "The term {} has been deleted with all its attached content"


  def delete(self, request, *args, **kwargs):
      obj = self.get_object()
      if obj.current == True:
        messages.warning(request, 'Cannot delete term as it is set to current')
        return redirect('terms')
      messages.success(self.request, self.success_message.format(obj.name))
      return super(TermDeleteView, self).delete(request, *args, **kwargs)

'''SESSIONS'''

class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
  model = AcademicSession
  fields = ['name', 'current']
  success_url = reverse_lazy('main:session-list')
  success_message = 'Session successfully updated.'
  template_name = 'corecode/mgt_form.html'


  def form_valid(self, form):
    obj = self.object
    if obj.current == False:
      terms = AcademicSession.objects.filter(
          current=True).exclude(name=obj.name).exists()
      if not terms:
        messages.warning(self.request, 'You must set a session to current.')
        return redirect('main:session-list')
    return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, DeleteView):
  model = AcademicSession
  success_url = reverse_lazy('main:session-list')
  template_name = 'corecode/core_confirm_delete.html'
  success_message = "The session {} has been deleted with all its attached content"


  def delete(self, request, *args, **kwargs):
      obj = self.get_object()
      if obj.current == True:
        messages.warning(request, 'Cannot delete session as it is set to current')
        return redirect('sessions')
      messages.success(self.request, self.success_message.format(obj.name))
      return super(SessionDeleteView, self).delete(request, *args, **kwargs)

class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
  form_class = AcademicSessionForm
  template_name = 'corecode/mgt_form.html'
  success_url = reverse_lazy('main:session-list')
  success_message = 'New session successfully added'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['title'] = 'Add new session'
      return context

class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
  model = AcademicSession
  template_name = 'corecode/session_list.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['form'] = AcademicSessionForm()
      return context

def home(request):
    return render(request, 'home.html')

def view_404(request, *args, **kwargs):
    return render(request,'partial/404.html',{'title':'Oops! Page Not Found!!'}, status=404)

class StudentListView(ListView):
    model = Student
    template_name = "students/student_list.html"
    paginate_by = 50
    context_object_name = 'students'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        clas = self.request.GET.get('class')
        sec = self.request.GET.get('sec')
        if clas is not None:
            qs = qs.filter(StudentProfile__Class=clas)
        if sec is not None:
            qs = qs.filter(StudentProfile__section=sec)
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["classes"] = Class.objects.all()
        context["sections"] = Section.objects.all()
        return context
    

class TeacherListView(ListView):
    model = Teacher
    template_name = "staffs/staff_list.html"
    paginate_by = 50
    context_object_name = 'teachers'


@staff_member_required(login_url='account_login')
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
    return render(request, 'students/student_form.html', context)

@staff_member_required(login_url='account_login')
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

@staff_member_required(login_url='account_login')
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


@staff_member_required(login_url='account_login')
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

class UserDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    login_url = 'accounts_login'
    model = User
    template_name = "administration/delete_object.html"

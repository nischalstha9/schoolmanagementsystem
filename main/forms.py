from django.forms import ModelForm, TextInput, ModelChoiceField, Form, modelformset_factory
from accounts.models import Student, StudentProfile, Teacher, TeacherProfile, Class, Section
from .models import AcademicSession, AcademicTerm, Subject, SiteConfig

SiteConfigForm = modelformset_factory(SiteConfig, fields=('key', 'value',), extra=0)

class AdmissionForm1(ModelForm):
    class Meta:
         model = Student
         fields = ['first_name', 'last_name']

class AdmissionForm2(ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['parent_name', 'contact', 'gender', 'date_of_birth', 'roll', 'Class', 'section', 'address','discount']
        widgets = {
            'date_of_birth': TextInput(attrs={'type':'date'}),
        }

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name']

class TeacherProfileForm(ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['address','major_subject','education','contact','salary']

class AcademicSessionForm(ModelForm):
  prefix = 'Academic Session'
  class Meta:
    model = AcademicSession
    fields = ['name','current']

class AcademicTermForm(ModelForm):
  prefix = 'Academic Term'
  class Meta:
    model = AcademicTerm
    fields = ['name','current']



class SubjectForm(ModelForm):
  prefix = 'Subject'
  class Meta:
    model = Subject
    fields = ['name']

class StudentClassForm(ModelForm):
  prefix = 'Class'
  class Meta:
    model = Class
    fields = ['std','fee']

class CurrentSessionForm(Form):
  current_session = ModelChoiceField(queryset=AcademicSession.objects.all(), help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session')
  current_term = ModelChoiceField(queryset=AcademicTerm.objects.all(), help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term')

from django.forms import ModelForm, TextInput
from accounts.models import Student, StudentProfile, Teacher, TeacherProfile, Class, Section

class AdmissionForm1(ModelForm):
    class Meta:
         model = Student
         fields = ['first_name', 'last_name']

class AdmissionForm2(ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['parent_name', 'contact', 'roll', 'Class', 'section', 'address','discount']

class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name']

class TeacherProfileForm(ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['address','major_subject','education','contact','salary']
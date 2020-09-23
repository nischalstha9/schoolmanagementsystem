from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import RegexValidator

class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    user=self._create_user(email, password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    class Types(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
        PARENT = "PARENT","Parent"

    base_type = Types.STUDENT

    _type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','_type']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self._type = self.base_type
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def get_absolute_url(self):
    #     return "/users/%i/" % (self.pk)

class TeacherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(_type=User.Types.TEACHER)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='TeacherProfile')
    address = models.CharField(max_length=255, null=True, blank=True)
    education = models.CharField(max_length=255, null=True, blank=True)
    major_subject = models.CharField(max_length=255, null=True, blank=True)
    mobile_num_regex      = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    contact  = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile (TEACHER)"

class Teacher(User):
    base_type = User.Types.TEACHER
    objects = TeacherManager()

    @property
    def profile(self):
        return self.TeacherProfile

    class Meta:
        proxy = True

class Section(models.Model):
    name = models.CharField(max_length = 10)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Section_detail", kwargs={"pk": self.pk})

class Class (models.Model):
    std = models.CharField(max_length=50)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    fee = models.IntegerField()

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"Class {self.std}"

class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(_type=User.Types.STUDENT)

class StudentProfile(models.Model):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="StudentProfile")#related_name is used to call object
    roll = models.IntegerField()
    Class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True, related_name='klas')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    address = models.CharField( max_length=200, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    parent_name = models.CharField(max_length = 254)
    gender = models.CharField(max_length=10, choices=GENDER, default='male')
    date_of_birth = models.DateField(default=timezone.now)
    date_of_admission = models.DateField(default=timezone.now)
    mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    contact  = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s Profile"

class Student(User):
    base_type = User.Types.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.StudentProfile
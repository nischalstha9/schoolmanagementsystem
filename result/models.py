from django.db import models
from main.models import AcademicSession, AcademicTerm, Subject
from accounts.models import Student, Class, Section
from .utils import score_grade

# Create your models here.
class Result(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
  term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
  current_class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
  current_section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
  subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
  test_score = models.IntegerField(default=0)
  exam_score = models.IntegerField(default=0)

  class Meta:
    ordering = ['subject']

  def __str__(self):
    return f'{self.student} {self.session} {self.term} {self.subject}'

  def total_score(self):
    return self.test_score + self.exam_score

  def grade(self):
    return score_grade(self.total_score())

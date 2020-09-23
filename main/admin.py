from django.contrib import admin
from .models import SiteConfig, AcademicSession, AcademicTerm, Subject

# Register your models here.
admin.site.register(SiteConfig)
admin.site.register(AcademicSession)
admin.site.register(AcademicTerm)
admin.site.register(Subject)
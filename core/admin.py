from django.contrib import admin
from .models import Certification, User, TestQuestions, TestAttempt, Reviews, Certificate, Gallery, Blog, SaveInfo

admin.site.register(Certification)
admin.site.register(TestQuestions)
admin.site.register(Reviews)
admin.site.register(Gallery)
admin.site.register(Blog)
admin.site.register(SaveInfo)

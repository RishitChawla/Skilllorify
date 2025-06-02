from django.contrib import admin
from .models import Certification, User, TestQuestions, TestAttempt, Reviews, Certificate, Gallery, Blog

admin.site.register(User)
admin.site.register(Certification)
admin.site.register(TestQuestions)
admin.site.register(TestAttempt)
admin.site.register(Reviews)
admin.site.register(Certificate)
admin.site.register(Gallery)
admin.site.register(Blog)
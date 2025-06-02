from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    
    # Auth
    # path('signup/', views.register_user, name='register'),
    # path('login/', views.login_user, name='login'),
    # path('logout/', views.logout_user, name='logout'),
    
    # Docs
    path('about-us/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('career/', views.career, name='career'),
    path('contact-us/', views.contactus, name='contactus'),
    path('thank-you/', views.thankyou, name='thankyou'),
    path('privacy-policy/', views.privacy, name='privacy'),
    path('terms-conditions/', views.terms, name='terms'),

    # Blog
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:blog_slug>', views.blogPost, name='blogPost'),
    path('dashboard/', views.edit, name='edit'),

    # Certification
    path('all-certifications/', views.all_certifications, name="all_certifications"),
    path('certification/<slug:cert_slug>/', views.certification, name='certification'),
    path('test-result/<slug:cert_slug>', views.submit_test, name="submit_test"),
    path('certification/<slug:cert_slug>/test/<uuid:test_uuid>/', views.test, name='test'),
    path('certification/<slug:cert_slug>/certificate/<uuid:test_uuid>', views.certificate, name='certificate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

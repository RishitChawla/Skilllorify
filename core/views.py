from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models import Q
import cv2
import uuid
import hashlib
from datetime import datetime
from markdown2 import Markdown
from .models import Certification, TestQuestions, TestAttempt, Reviews, Certificate, Gallery, Blog
from natsort import natsorted


import os
from pdf2image import convert_from_path
from django.conf import settings

import logging
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    card = Certification.objects.filter(popular=True)[:3]
    
    return render(request, "core/index.html", {
        "card": card,
    })


# def register_user(request):
#     if request.user.is_authenticated:
#         return reverse("index")
    
#     if request.method == "POST":
#         if "registerBtn" in request.POST:
#             name = request.POST.get("name")
#             email = request.POST.get("email")
#             phone = request.POST.get("phone")
#             password = request.POST.get("password")
#             confirmPassword = request.POST.get("confirmPassword")

#             if password != confirmPassword:
#                 return render(request, "auth/register.html", {
#                 "message": "Passwords must match."
#             })
#             try:
#                 user = User.objects.create_user(
#                     username = name,
#                     email = email,
#                     phone = phone,
#                     password = password
#                 )
#                 user.save()
#             except IntegrityError:
#                 return render(request, "auth/register.html", {
#                     "message": "Username already taken."
#                 })
#             login(request, user)
#             return HttpResponseRedirect(reverse("index"))

#     return render(request, "auth/register.html")


# def login_user(request):
#     return render(request, "auth/login.html")


# @login_required
# def logout_user(request):
#     try:
#         logout(request)
#         return HttpResponseRedirect(reverse("index"))
#     except:
#         return HttpResponseRedirect(reverse("index"))
    
def all_certifications(request):
    queryset = Certification.objects.all().order_by('-createdAt')

    if request.method == "GET" and "apply" in request.GET:
        search = request.GET.get('search', '').strip()
        difficulty = request.GET.get('difficulty', '').strip()
        sort_by = request.GET.get('sort_by', '').strip()
        min_price = request.GET.get('min')
        max_price = request.GET.get('max')

        # Search filter
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(bio__icontains=search)
            )

        # Difficulty filter
        if difficulty:
            queryset = queryset.filter(difficulty__iexact=difficulty)

        # Price range filter
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Sorting
        if sort_by == 'newest':
            queryset = queryset.order_by('-createdAt') 
        elif sort_by == 'price-low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price-high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-rating')  

    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'card': page_obj,
        'paginator': paginator,
    }

    return render(request, 'dynamic/allCertifications.html', context)

def edit(request):
    return render(request, "admin/edit.html")


import glob
def certification(request, cert_slug):
    details = get_object_or_404(Certification, slug=cert_slug)
    reviews = Reviews.objects.filter(certification=details)
    more = Certification.objects.order_by('?')[:3]
    questions = TestQuestions.objects.filter(certification=details)

    

    if request.method == "POST":
        if "enrollBtn" in request.POST:
            if details.price <= 0 or details.discountedPrice <= 0:
                request.session[f'allow_certification_{cert_slug}'] = True
                return redirect(reverse('content', kwargs={'cert_slug': cert_slug}))

            else:
                return HttpResponse("Razorpay Portal")
        
        if "takeTestBtn" in request.POST:
            return render(request, "dynamic/test.html", {
                "questions": questions,
            })

    return render(request, "dynamic/certification.html", {
        "course": details,
        "reviews": reviews,
        "more": more,
    })



def content(request, cert_slug):
    access_key = f'allow_certification_{cert_slug}'

    if not request.session.get(access_key, False):
        return HttpResponseForbidden("🚫 You can't access this page directly.")

    details = get_object_or_404(Certification, slug=cert_slug)

    image_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images', cert_slug)
    image_files = natsorted(
        glob.glob(os.path.join(image_dir, '*.png')) +
        glob.glob(os.path.join(image_dir, '*.jpeg')) +
        glob.glob(os.path.join(image_dir, '*.jpg'))
    )

    image_urls = [
        f'/media/pdf_images/{cert_slug}/{os.path.basename(img)}'
        for img in image_files
    ]

    paginator = Paginator(image_urls, 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "dynamic/content.html", {
        "course": details,
        "page_obj": page_obj,
    })


def test(request, cert_slug, test_uuid):
    details = get_object_or_404(Certification, slug=cert_slug)

    # if testState.active == False:
        # return HttpResponse("This test has ended")

    return render(request, "dynamic/test.html", {
        "course": details,
    })


def submit_test(request, cert_slug):
    certification = get_object_or_404(Certification, slug=cert_slug)
    questions = TestQuestions.objects.filter(certification=certification)
    time = datetime.now()

    if request.method == 'POST':
        correct = 0
        total = questions.count()
        try:
            for question in questions:
                selected = request.POST.get(f'question-{question.id}')
                if selected and selected == question.correct_option:
                    correct += 1
            score_percent = (correct / total) * 100
            passed = score_percent >= 50

            attempt = TestAttempt.objects.create(
                score=score_percent,
                passed=passed
            )

            if "submit" in request.POST:
                return render(request, 'dynamic/result.html', {
                    "certification": certification,
                    'score': score_percent,
                    'passed': passed,
                    'total': total,
                    'correct': correct,
                    'incorrect': total-correct,
                    'attempt_uuid': attempt.uuid
                })

            if "view" in request.POST:
                name = request.POST.get("name")
                email = request.POST.get("email")
                phone = request.POST.get("phone")
                data = str(time.time()).encode()
                unique_id = hashlib.sha256(data).hexdigest()[:16]

                certificate = Certificate.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    certID=unique_id
                )

                

                # (0, 93, 173)
                template_path = rf"/home/ubuntu/Skilllorify/core/static/images/template/2Certificate.png"
                logger.info("📂 Reading template from:", template_path)

                template = cv2.imread(template_path)

                # 🛑 DEBUG CHECK
                if template is None:
                    logger.error("❌ ERROR: Could not read template image!")
                else:
                    logger.info("✅ Image read successfully!")


                #template = cv2.imread(rf"/home/ubuntu/Skilllorify/core/static/images/template/2.png")
                #print("Reading template from:", rf"/home/ubuntu/Skilllorify/core/static/images/template/2.png")
                cv2.putText(template, name, (760, 1830), cv2.FONT_HERSHEY_COMPLEX, 4, (30, 60, 114), 10, cv2.LINE_AA)
                cv2.putText(template, certification.name, (530, 2240), cv2.FONT_HERSHEY_COMPLEX, 1.6, (30, 60, 114), 5, cv2.LINE_AA)
                cv2.putText(template, time.strftime("%d"), (1160, 2410), cv2.FONT_HERSHEY_COMPLEX, 2, (30, 60, 114), 7, cv2.LINE_AA)
                cv2.putText(template, time.strftime("%m"), (1300, 2410), cv2.FONT_HERSHEY_COMPLEX, 2, (30, 60, 114), 7, cv2.LINE_AA)
                cv2.putText(template, str(time.year), (1445, 2410), cv2.FONT_HERSHEY_COMPLEX, 2, (30, 60, 114), 7, cv2.LINE_AA)
                cv2.putText(template, unique_id, (700, 2950), cv2.FONT_HERSHEY_COMPLEX, 1, (30, 60, 114), 3, cv2.LINE_AA)
                cv2.imwrite(rf'/home/ubuntu/Skilllorify/media/images/certificates/{name}-{certification.name}.jpg', template)
                return render(request, "dynamic/certificate.html", {
                    "certification": certification,
                    "name": f"{name}-{certification.name}.jpg",
                })
        
        except Exception  as e:
            return HttpResponse(f"Error: {e}")
        
    return HttpResponse("Invalid submit type")


def certificate(request, uuid):
    attempt = get_object_or_404(TestAttempt, uuid=uuid)
    return render(request, 'dynamic/certificate.html', {'attempt': attempt})


def about(request):
    return render(request, "docs/about.html")

def contactus(request):
    return render(request, "docs/contactus.html")

def thankyou(request):
    return render(request, "docs/thankyou.html")

def career(request):
    return render(request, "docs/career.html")

def gallery(request):
    images = Gallery.objects.all()

    return render(request, "docs/gallery.html", {
        "gallery" : images
    })

def privacy(request):
    return render(request, "docs/privacy.html")

def terms(request):
    return render(request, "docs/terms.html")

def blog(request):
    blogs = Blog.objects.all()

    # Pagination
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'blogs': page_obj,
        'paginator': paginator,
    }

    return render(request, 'blog/blog.html', context)


def blogPost(request, blog_slug):
    blog = get_object_or_404(Blog, slug=blog_slug) 

    content = Markdown().convert(blog.content)

    return render(request, "blog/blog-post.html", {
        "blog": blog,
        "content": content
    })



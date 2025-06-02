from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True, null=True, blank=True)  
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    REQUIRED_FIELDS = ['phone', 'name', "email"]  

    def __str__(self):
        return self.email


class Certification(models.Model):
    name = models.CharField(max_length=124, unique=True)
    poster = models.ImageField(upload_to="images/poster", max_length=500)
    bio = models.CharField(max_length=100, default="")
    price = models.IntegerField(default=0)
    discountedPrice = models.IntegerField(blank=True, null=True)
    difficulty = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')],
    )
    duration = models.CharField(max_length=50, default="")
    rating = models.FloatField(default=4.8,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ])
    popular = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Reviews(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name="Certification")
    name = models.CharField(max_length=20)
    pfp = models.ImageField(upload_to="images/reviewspfp", max_length=500)
    rating = models.FloatField()
    review = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

class TestQuestions(models.Model):
    certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name="certification")
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
    )

    def __str__(self):
        return self.question
    


class TestAttempt(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    score = models.FloatField()
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.uuid}"
    

class Certificate(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    certID = models.CharField(max_length=20, null=True, blank=True)


class Gallery(models.Model):
    topic = models.CharField(max_length=124)
    bio = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Blog(models.Model):
    topic = models.CharField(max_length=255)
    bio = models.CharField(max_length=2058)
    category = models.CharField(max_length=100)
    poster = models.ImageField(upload_to="images/blogPoster", max_length=500)
    length = models.IntegerField(default=5)
    author = models.CharField(max_length=100, default=None)
    content = models.TextField()
    isFeatured = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.topic)
        super().save(*args, **kwargs)

    created_at = models.DateTimeField(auto_now_add=True)

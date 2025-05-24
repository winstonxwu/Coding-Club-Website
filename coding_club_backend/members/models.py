from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class MemberManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        username = email.split('@')[0]
        
        base_username = username
        counter = 1
        while self.model.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('account_type', 'teacher')
        return self.create_user(email, password, **extra_fields)

class Member(AbstractUser):
    ACCOUNT_TYPES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='student')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    grade = models.IntegerField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['account_type']
    
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)

    objects = MemberManager()

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            base_username = self.email.split('@')[0]
            username = base_username
            counter = 1
            while Member.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Meeting(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='created_meetings')
    ai_summary = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='attendances')
    is_present = models.BooleanField(default=False)
    recorded_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='recorded_attendances')
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['meeting', 'student']
        ordering = ['meeting', 'student']

    def __str__(self):
        status = "Present" if self.is_present else "Absent"
        return f"{self.student} - {self.meeting} - {status}"
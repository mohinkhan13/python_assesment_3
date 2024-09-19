from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator
from django.utils import timezone


class CustomUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$')], unique=True, default='')
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('User', 'User')] ,default='User')

    def __str__(self):
        return self.username
# Create your models here.

class CustomerQuestion(models.Model):
    QUESTION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to CustomUser if needed
    question_text = models.TextField()
    status = models.CharField(max_length=10, choices=QUESTION_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.question_text[:50]  # Display the first 50 characters

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)      

    def __str__(self):
        return self.name  

class Policy(models.Model):
    policy_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.policy_name

class PolicyHolder(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    policies = models.ManyToManyField(Policy, through='PolicyHolderPolicy')

    def __str__(self):
        return self.user.username

class PolicyHolderPolicy(models.Model):
    policy_holder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Due', 'Due')])
    approval_status = models.CharField(
        max_length=10,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
        )
    def __str__(self):
        return f"{self.policy_holder} - {self.policy}"    
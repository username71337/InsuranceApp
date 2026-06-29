from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('consultant', 'Consultant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_consultant(self):
        return self.role == 'consultant'

    def is_member(self):
        return self.role == 'member'

    def __str__(self):
        return f"{self.username} ({self.role})"


class ConsultantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultant_profile')
    company_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    profile_photo = models.ImageField(upload_to='consultants/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name} — {self.user.get_full_name()}"


# ── Life Insurance ──────────────────────────────────────────────────────────────

class LifePlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('term', 'Term Life'),
        ('whole', 'Whole Life'),
        ('universal', 'Universal Life'),
        ('variable', 'Variable Life'),
        ('endowment', 'Endowment'),
    ]
    consultant = models.ForeignKey(
        ConsultantProfile, on_delete=models.CASCADE, related_name='life_plans'
    )
    name = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=30, choices=PLAN_TYPE_CHOICES)
    description = models.TextField()
    coverage_amount_min = models.DecimalField(max_digits=15, decimal_places=2)
    coverage_amount_max = models.DecimalField(max_digits=15, decimal_places=2)
    premium_from = models.DecimalField(max_digits=10, decimal_places=2)
    premium_period = models.CharField(max_length=20, default='monthly')
    age_min = models.PositiveIntegerField(default=18)
    age_max = models.PositiveIntegerField(default=65)
    term_years = models.PositiveIntegerField(blank=True, null=True, help_text='For term plans')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()}) — {self.consultant.company_name}"


class LifePolicy(models.Model):
    plan = models.ForeignKey(LifePlan, on_delete=models.CASCADE, related_name='policies')
    policy_number = models.CharField(max_length=100, unique=True)
    holder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='life_policies')
    beneficiary_name = models.CharField(max_length=200)
    beneficiary_relationship = models.CharField(max_length=100)
    coverage_amount = models.DecimalField(max_digits=15, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Policy #{self.policy_number} — {self.holder.username}"


# ── Non-Life Insurance ──────────────────────────────────────────────────────────

class NonLifePlan(models.Model):
    CATEGORY_CHOICES = [
        ('motor', 'Motor Vehicle'),
        ('property', 'Property / Fire'),
        ('health', 'Health & Medical'),
        ('travel', 'Travel'),
        ('marine', 'Marine / Cargo'),
        ('liability', 'Liability'),
        ('business', 'Business / Commercial'),
    ]
    consultant = models.ForeignKey(
        ConsultantProfile, on_delete=models.CASCADE, related_name='non_life_plans'
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.TextField()
    coverage_details = models.TextField(help_text='What is covered')
    exclusions = models.TextField(blank=True, help_text='What is NOT covered')
    premium_from = models.DecimalField(max_digits=10, decimal_places=2)
    premium_period = models.CharField(max_length=20, default='annual')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) — {self.consultant.company_name}"


class NonLifePolicy(models.Model):
    plan = models.ForeignKey(NonLifePlan, on_delete=models.CASCADE, related_name='policies')
    policy_number = models.CharField(max_length=100, unique=True)
    holder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='non_life_policies')
    insured_item = models.CharField(max_length=300, help_text='Vehicle plate, property address, etc.')
    coverage_amount = models.DecimalField(max_digits=15, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Policy #{self.policy_number} — {self.holder.username}"


# ── Consultation Request ────────────────────────────────────────────────────────

class ConsultationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    consultant = models.ForeignKey(
        ConsultantProfile, on_delete=models.CASCADE, related_name='consultation_requests'
    )
    member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='consultation_requests'
    )
    full_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True, help_text='Optional message or inquiry')
    interested_in = models.CharField(
        max_length=10,
        choices=[('life', 'Life Insurance'), ('nonlife', 'Non-Life Insurance'), ('both', 'Both')],
        default='both',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} → {self.consultant.company_name} [{self.status}]"


# ── Messaging ───────────────────────────────────────────────────────────────────

class Conversation(models.Model):
    consultation = models.OneToOneField(
        ConsultationRequest, on_delete=models.CASCADE, related_name='conversation'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation: {self.consultation}"

    def last_message(self):
        return self.messages.order_by('-sent_at').first()


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"{self.sender.username}: {self.body[:50]}"

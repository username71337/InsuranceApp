from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, ConsultantProfile,
    LifePlan, LifePolicy,
    NonLifePlan, NonLifePolicy,
    ConsultationRequest, Conversation, Message
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Contact', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role & Contact', {'fields': ('role', 'phone', 'email')}),
    )


@admin.register(ConsultantProfile)
class ConsultantProfileAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'license_number', 'years_experience', 'is_available']
    list_filter = ['is_available']
    search_fields = ['company_name', 'user__username', 'user__email']


@admin.register(LifePlan)
class LifePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'consultant', 'premium_from', 'is_active']
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name', 'consultant__company_name']


@admin.register(LifePolicy)
class LifePolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'holder', 'plan', 'coverage_amount', 'is_active']
    list_filter = ['is_active']
    search_fields = ['policy_number', 'holder__username']


@admin.register(NonLifePlan)
class NonLifePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'consultant', 'premium_from', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'consultant__company_name']


@admin.register(NonLifePolicy)
class NonLifePolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'holder', 'plan', 'coverage_amount', 'is_active']
    list_filter = ['is_active']
    search_fields = ['policy_number', 'holder__username']


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'consultant', 'member', 'interested_in', 'status', 'created_at']
    list_filter = ['status', 'interested_in']
    search_fields = ['full_name', 'consultant__company_name', 'member__username']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'consultation', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'conversation', 'sent_at', 'is_read']
    list_filter = ['is_read']

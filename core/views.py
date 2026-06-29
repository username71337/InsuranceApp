from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import (
    User, ConsultantProfile, LifePlan, NonLifePlan,
    ConsultationRequest, Conversation, Message
)
from .forms import (
    MemberSignUpForm, ConsultantSignUpForm,
    ConsultationRequestForm, MessageForm
)


# ── Home / Landing ──────────────────────────────────────────────────────────────

def home(request):
    consultants = ConsultantProfile.objects.filter(is_available=True).select_related('user')
    consultant_data = []
    for c in consultants:
        life_plans = c.life_plans.filter(is_active=True)
        non_life_plans = c.non_life_plans.filter(is_active=True)
        consultant_data.append({
            'profile': c,
            'life_plans': life_plans,
            'non_life_plans': non_life_plans,
        })
    return render(request, 'core/home.html', {'consultant_data': consultant_data})


# ── Auth ────────────────────────────────────────────────────────────────────────

def signup_choose(request):
    return render(request, 'core/signup_choose.html')


def member_signup(request):
    if request.method == 'POST':
        form = MemberSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your member account is ready.')
            return redirect('home')
    else:
        form = MemberSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'role': 'Member', 'role_key': 'member'})


def consultant_signup(request):
    if request.method == 'POST':
        form = ConsultantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your consultant profile is live.')
            return redirect('home')
    else:
        form = ConsultantSignUpForm()
    return render(request, 'core/signup.html', {'form': form, 'role': 'Consultant', 'role_key': 'consultant'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect(request.GET.get('next', 'home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ── Consultant Detail ───────────────────────────────────────────────────────────

def consultant_detail(request, pk):
    consultant = get_object_or_404(ConsultantProfile, pk=pk)
    life_plans = consultant.life_plans.filter(is_active=True)
    non_life_plans = consultant.non_life_plans.filter(is_active=True)
    return render(request, 'core/consultant_detail.html', {
        'consultant': consultant,
        'life_plans': life_plans,
        'non_life_plans': non_life_plans,
    })


# ── Consultation Request ────────────────────────────────────────────────────────

@login_required
def consult_request(request, consultant_pk):
    if request.user.is_consultant():
        messages.error(request, 'Consultants cannot send consultation requests.')
        return redirect('home')

    consultant = get_object_or_404(ConsultantProfile, pk=consultant_pk)

    # Check if already has an open request
    existing = ConsultationRequest.objects.filter(
        member=request.user, consultant=consultant, status__in=['pending', 'accepted']
    ).first()
    if existing:
        messages.info(request, 'You already have an active consultation with this consultant.')
        return redirect('conversation_detail', pk=existing.conversation.pk)

    if request.method == 'POST':
        form = ConsultationRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.member = request.user
            req.consultant = consultant
            req.save()
            # Auto-create conversation
            Conversation.objects.create(consultation=req)
            messages.success(request, f'Consultation request sent to {consultant.company_name}!')
            return redirect('my_consultations')
    else:
        form = ConsultationRequestForm(initial={
            'full_name': request.user.get_full_name(),
            'contact_number': request.user.phone,
            'email': request.user.email,
        })
    return render(request, 'core/consult_request.html', {
        'form': form,
        'consultant': consultant,
    })


@login_required
def my_consultations(request):
    if request.user.is_member():
        reqs = ConsultationRequest.objects.filter(member=request.user).select_related(
            'consultant__user', 'conversation'
        )
        return render(request, 'core/my_consultations.html', {'requests': reqs, 'role': 'member'})
    else:
        reqs = ConsultationRequest.objects.filter(consultant=request.user.consultant_profile).select_related(
            'member', 'conversation'
        )
        return render(request, 'core/my_consultations.html', {'requests': reqs, 'role': 'consultant'})


@login_required
def update_consultation_status(request, pk, status):
    req = get_object_or_404(ConsultationRequest, pk=pk, consultant=request.user.consultant_profile)
    if status in ['accepted', 'declined', 'completed']:
        req.status = status
        req.save()
        if status == 'accepted' and not hasattr(req, 'conversation'):
            Conversation.objects.create(consultation=req)
        messages.success(request, f'Request marked as {status}.')
    return redirect('my_consultations')


# ── Messaging ───────────────────────────────────────────────────────────────────

@login_required
def conversation_detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    consultation = conversation.consultation

    # Access check
    is_member = request.user == consultation.member
    is_consultant = (
        hasattr(request.user, 'consultant_profile') and
        request.user.consultant_profile == consultation.consultant
    )
    if not (is_member or is_consultant):
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('home')

    # Mark unread messages as read
    conversation.messages.exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.save()
            return redirect('conversation_detail', pk=pk)
    else:
        form = MessageForm()

    return render(request, 'core/conversation.html', {
        'conversation': conversation,
        'consultation': consultation,
        'msgs': conversation.messages.all(),
        'form': form,
        'is_consultant': is_consultant,
    })


# ── Dashboard ───────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    if request.user.is_consultant():
        profile = get_object_or_404(ConsultantProfile, user=request.user)
        pending = ConsultationRequest.objects.filter(consultant=profile, status='pending').count()
        active = ConsultationRequest.objects.filter(consultant=profile, status='accepted').count()
        life_count = profile.life_plans.filter(is_active=True).count()
        nonlife_count = profile.non_life_plans.filter(is_active=True).count()
        recent_requests = ConsultationRequest.objects.filter(consultant=profile).order_by('-created_at')[:5]
        return render(request, 'core/dashboard.html', {
            'profile': profile,
            'pending': pending,
            'active': active,
            'life_count': life_count,
            'nonlife_count': nonlife_count,
            'recent_requests': recent_requests,
        })
    else:
        my_requests = ConsultationRequest.objects.filter(member=request.user).order_by('-created_at')[:5]
        life_policies = request.user.life_policies.filter(is_active=True)
        nonlife_policies = request.user.non_life_policies.filter(is_active=True)
        return render(request, 'core/dashboard.html', {
            'my_requests': my_requests,
            'life_policies': life_policies,
            'nonlife_policies': nonlife_policies,
        })

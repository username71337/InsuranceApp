from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ConsultantProfile, ConsultationRequest, Message


class MemberSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'member'
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user


class ConsultantSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    company_name = forms.CharField(max_length=200, required=True)
    license_number = forms.CharField(max_length=100, required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    years_experience = forms.IntegerField(min_value=0, initial=0, required=False)
    specialization = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'consultant'
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
            ConsultantProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                license_number=self.cleaned_data.get('license_number', ''),
                bio=self.cleaned_data.get('bio', ''),
                years_experience=self.cleaned_data.get('years_experience') or 0,
                specialization=self.cleaned_data.get('specialization', ''),
            )
        return user


class ConsultationRequestForm(forms.ModelForm):
    class Meta:
        model = ConsultationRequest
        fields = ['full_name', 'contact_number', 'email', 'interested_in', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any specific questions or concerns?'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'contact_number': forms.TextInput(attrs={'placeholder': '+63 9XX XXX XXXX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Type your message…',
                'class': 'msg-input',
            })
        }
        labels = {'body': ''}

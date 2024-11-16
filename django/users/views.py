
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userprofile

        # Update email
        user.email = request.POST.get('email')
        user.save()

        # Update profile fields
        profile.phone_number = request.POST.get('phone_number')
        profile.preferred_currency = request.POST.get('preferred_currency')
        profile.notification_enabled = request.POST.get('notification_enabled') == 'on'
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')

    return redirect('users:profile')
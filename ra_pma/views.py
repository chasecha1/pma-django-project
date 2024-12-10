from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login
from events.models import Event
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
import json
from .decorators import ra_required, restrict_roles

from django.forms import ModelForm
from .models import UserProfile


def set_role_and_login(request):
    if request.method == 'POST':
        role = request.POST.get('role', 'common')  # Default to 'common' if not provided
        request.session['role'] = role  # Store the role in the session

        # Redirect to the Google OAuth login URL
        return redirect(reverse('social:begin', args=['google-oauth2']))

    return redirect('login')  # If accessed via GET, redirect to the login page

@login_required
def save_background_color(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        background_color = data.get('background_color', '#FFFFFF')
        # Save the color in the user's session
        request.session['background_color'] = background_color

        # save it in the user's profile
        user_profile = request.user.userprofile
        user_profile.background_color = background_color
        user_profile.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

@login_required
def dashboard(request):
    # Get the role from the session
    role = request.session.get('role', 'common')  # Default to 'common' if not set
    user_profile = request.user.userprofile

    # Update the user's role only if it matches the session role
    if role == 'admin' and not user_profile.is_admin:
        user_profile.is_admin = True
        user_profile.is_RA = user_profile.is_SR = False
    elif role == 'ra' and not user_profile.is_RA:
        user_profile.is_RA = True
        user_profile.is_admin = user_profile.is_SR = False
    elif role == 'sr' and not user_profile.is_SR:
        user_profile.is_SR = True
        user_profile.is_admin = user_profile.is_RA = False

    # Only save changes if there's an actual update
    user_profile.save()

    # Get the background color from the user's profile
    background_color = user_profile.background_color or '#FFFFFF'
    request.session['background_color'] = background_color

    # Redirect based on the updated profile
    if user_profile.is_admin or user_profile.is_SR:
        return redirect('admin_dashboard')
    elif user_profile.is_RA:
        return redirect('ra_dashboard')
    else:
        return redirect('common_dashboard')


@login_required
def admin_dashboard(request):
    background_color = request.session.get('background_color', '#FFFFFF')
    context = {
        "page_title": "Admin Dashboard",
        "background_color": background_color,
    }
    # return HttpResponseRedirect('/admin')
    return render(request, 'ra_pma/admin_dash.html', context)

@login_required
@ra_required
def ra_dashboard(request):
    background_color = request.session.get('background_color', '#FFFFFF')
    context = {
        "page_title": "RA Dashboard",
        "background_color": background_color,
    }
    return render(request, 'ra_pma/admin_dash.html', context)

@login_required
@restrict_roles(disallowed_roles=['ra'], redirect_to='ra_dashboard')
def common_dashboard(request):
    background_color = request.session.get('background_color', '#FFFFFF')
    all_events = Event.objects.exclude(
        Q(members=request.user) | Q(user=request.user)
    ).order_by('-date')
    my_events = Event.objects.filter(user=request.user).order_by('date')
    joined_events = Event.objects.filter(members=request.user).order_by('date')
    context = {
        "page_title": "Common Dashboard",
        "all_events": all_events,
        "my_events": my_events,
        "joined_events": joined_events,
        "background_color": background_color,
    }
    return render(request, 'ra_pma/common_dash.html', context)

def redirect_root_url(request):
    return redirect('/login')

def login_choice(request):
    return render(request, 'ra_pma/login.html')


def anonymous_view(request):
    # Fetch events without clickable links
    event = Event.objects.all().order_by('-date')  # Adjust as needed to get the events
    context = {'events': event}
    return render(request, 'ra_pma/anonymous_dash.html', context)


def profile_view(request):
    return render(request, 'ra_pma/profile.html', {'user': request.user})


def setting_view(request):
    if request.user.is_authenticated:
        background_color = request.user.userprofile.background_color or '#FFFFFF'
    else:
        background_color = '#FFFFFF'
    return render(request, 'ra_pma/setting.html', {'user': request.user, 'background_color': background_color})


def contact_view(request):
    return render(request, 'ra_pma/resources.html', {'user': request.user})


def notification_view(request):
    return render(request, 'ra_pma/notification.html', {'user': request.user})


# https://docs.djangoproject.com/en/dev/topics/http/views/#customizing-error-views
def custom_404(request, exception):
    return render(request, 'ra_pma/error.html', {'error_code': 404})


def custom_403(request, exception):
    return render(request, 'ra_pma/error.html', {'error_code': 403})


def custom_500(request):
    return render(request, 'ra_pma/error.html', {'error_code': 500})


def custom_400(request, exception):
    return render(request, 'ra_pma/error.html', {'error_code': 400})


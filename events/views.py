from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Event, File
from .forms import FileForm, MessageForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from ra_pma.models import User
from django.db.models import Q

# Processing and getting the data from the add event form
@login_required
@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON body'}, status=400)

        # Check if all required fields are present and not empty
        required_fields = ['title', 'date', 'description']
        for field in required_fields:
            if field not in data or not data[field].strip():  # Ensure the field is not empty
                return JsonResponse({'status': 'error', 'message': 'Missing or invalid required fields'}, status=400)

        # Create the event
        new_event = Event.objects.create(
            user=request.user,
            title=data['title'],
            date=data['date'],
            description=data['description']
        )
        return JsonResponse({'status': 'success', 'message': 'Event added successfully'})

    # Handle other methods
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# Function to get events for a specific month
@login_required
def get_calendar_events(request, year_month):
    """
    Fetch events for the given month that the logged-in user created or successfully joined.
    """
    try:
        # Split the year and month from the parameter
        year, month = map(int, year_month.split('-'))
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM.'}, status=400)

    # Query events created by the user or joined by the user
    events = Event.objects.filter(
        Q(user=request.user) | Q(members=request.user),  # Created or successfully joined
        date__year=year,
        date__month=month
    ).values('id', 'title', 'date', 'description')  # Only return necessary fields

    # Convert the queryset to a list and return as JSON
    return JsonResponse(list(events), safe=False)

@login_required
def delete_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({'success': True})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)

@login_required
def delete_file(request, file_id):
    try:
        file = get_object_or_404(File, id=file_id)

        # Only allow file owner or users with specific roles to delete
        if file.user != request.user and not request.user.userprofile.is_RA:
            return JsonResponse({'error': 'Unauthorized: You do not have permission to delete this file.'}, status=403)

        file.delete()
        return JsonResponse({'success': True})
    except File.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)


def get_events(request):
    if request.method == 'GET':
        events = Event.objects.all().values('id', 'title', 'date', 'description').order_by('date')  # Fetch all events
        events_list = list(events)
        return JsonResponse({'events': events_list})
    
@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    file_form = FileForm()
    message_form = MessageForm()

    if request.method == 'POST':
        if 'file_upload' in request.POST:
            # Handle file upload
            file_form = FileForm(request.POST, request.FILES)
            if file_form.is_valid():
                file = file_form.save(commit=False)
                file.event = event  # Associate file with the event
                file.user = request.user  # Set the user who uploaded the file
                file.save()
                # Redirect using namespace
                return redirect('event_detail', event_id=event.id)
        elif 'message_post' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.event = event  # Associate message with the event
                message.user = request.user  # Set the user who posted the message
                message.save()
                return redirect('event_detail', event_id=event.id)

    files = event.files.all()
    messages = event.messages.all().order_by('uploaded_at')

    return render(request, 'events/event_detail.html', {
        'page_title': event,
        'event': event,
        'file_form': file_form,
        'message_form': message_form,
        'files': files,
        'messages': messages,
    })


@login_required
def request_to_join(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user == event.user:
        return JsonResponse({'status': 'error', 'message': 'You cannot request to join your own event.'})  # or wherever you want to redirect

    if request.user in event.members.all():
        messages.error(request, "You are already a member of this event.")
        return JsonResponse({'status': 'error', 'message': 'You are already a member of this event.'})

    if request.user in event.requests.all():
        return JsonResponse({'status': 'error', 'message': 'You cannot request to join this event.'})

    # Add user to the requests
    event.requests.add(request.user)
    event.save()

    return JsonResponse({'success': True, 'message': "Your request to join the event has been submitted."})

@login_required
def approve_request(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)

    user_to_approve = get_object_or_404(User, id=user_id)

    # Add the user to the event members and remove from requests
    event.members.add(user_to_approve)
    event.requests.remove(user_to_approve)
    event.save()

    messages.success(request, f"{user_to_approve.username} has been added as a member of the event.")
    return redirect('event_detail', event_id=event.id)

def reject_request(request, event_id, user_id):
    event = get_object_or_404(Event, id=event_id)

    user_to_reject = get_object_or_404(User, id=user_id)

    # Remove the user from requests
    event.requests.remove(user_to_reject)
    event.save()

    messages.success(request, f"{user_to_reject.username} has been rejected from joining the event.")
    return redirect('event_detail', event_id=event.id)

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.members.all():
        event.members.remove(request.user)
    else:
        messages.error(request, "You are not a member of this event.")

    return redirect('dashboard')  # Replace 'dashboard' with the name of your dashboard view.

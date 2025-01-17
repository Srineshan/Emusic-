# myapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm,SignupForm
from myproject import settings
import logging
from urllib.parse import urlencode
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .models import Notification

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


def subscription(request):
    return render(request, 'subscription.html')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Log the user in automatically
            messages.success(request, 'Signup successful! You are now logged in.')
            return redirect('login')  # Redirect to the home page or any other page
        else:
            messages.error(request, 'There was an error in your form. Please try again.')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})



def base(request):
    return render(request, 'base.html')
# Login View
def login_v(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(profilehome)  # Redirect to home after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)  # This will log out the user
    return redirect('home')


@login_required
def help_center(request):
    return render(request, 'helpcentre.html')

def help_center1(request):
    return render(request, 'helpcentre1.html')




''' from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ProfileSettingsForm, CustomPasswordChangeForm
from .models import ProfileSettings


@login_required
def settings_view(request):
    # Get or create the user's profile settings (this avoids DoesNotExist error)
    profile_settings, created = ProfileSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle the profile settings and password forms
        profile_form = ProfileSettingsForm(request.POST, request.FILES, instance=profile_settings)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            # Save the profile settings form (including the profile picture if uploaded)
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('settings')  # Redirect to prevent resubmission on refresh

        if 'change_password' in request.POST and password_form.is_valid():
            # Change the password and update the session to keep the user logged in
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Password changed successfully!")
            return redirect('settings')  # Redirect after password change

    else:
        # For GET requests, initialize the forms with the current user's data
        profile_form = ProfileSettingsForm(instance=profile_settings)
        password_form = CustomPasswordChangeForm(request.user)

    # Render the settings page with the forms
    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'password_form': password_form
    }) '''
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileSettingsForm, CustomPasswordChangeForm
from .models import ProfileSettings, Notification

@login_required
def settings_view(request):
    # Get or create the user's profile settings
    profile_settings, created = ProfileSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle the profile settings and password forms
        profile_form = ProfileSettingsForm(request.POST, request.FILES, instance=profile_settings)
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            # Save the profile settings form (including the profile picture if uploaded)
            old_profile = ProfileSettings.objects.get(id=profile_settings.id)
            profile_form.save()

            # Check for changes in the fields and create notifications
            changes = []
            if old_profile.bio != profile_settings.bio:
                changes.append('Bio')
            if old_profile.location != profile_settings.location:
                changes.append('Location')
            if old_profile.profile_photo != profile_settings.profile_photo:
                changes.append('Profile Picture')

            # If there are changes, create a notification
            if changes:
                message = f"Profile updated successfully! Changed fields: {', '.join(changes)}."
                Notification.objects.create(
                    user=request.user,
                    message=message
                )
                messages.success(request, message)
            else:
                messages.info(request, "No changes were made to your profile.")
            
            return redirect('settings')  # Redirect to prevent resubmission on refresh

        if 'change_password' in request.POST and password_form.is_valid():
            # Change the password and update the session to keep the user logged in
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Password changed successfully!")
            return redirect('settings')  # Redirect after password change

    else:
        # For GET requests, initialize the forms with the current user's data
        profile_form = ProfileSettingsForm(instance=profile_settings)
        password_form = CustomPasswordChangeForm(request.user)

    # Render the settings page with the forms
    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })


SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

logger = logging.getLogger(__name__)

def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id = settings.SPOTIFY_CLIENT_ID,
        client_secret = settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri = settings.SPOTIFY_REDIRECT_URI,
        scope = 'user-library-read',
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    sp_oauth = SpotifyOAuth(
        client_id = settings.SPOTIFY_CLIENT_ID,
        client_secret = settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri = settings.SPOTIFY_REDIRECT_URI,
    )
    token_info = sp_oauth.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_data = sp.current_user()
    return render(request, 'spotifyprofile.html', {'user_data': user_data})



@login_required
def notifications_view(request):
    # Fetch all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'notifications.html', {
        'notifications': notifications
    })


from django.http import JsonResponse

@login_required
def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'})
    
@login_required
def profilehome(request):
    return render(request,'profilehome.html')




'''from django.shortcuts import render
from .spotify_helper import get_spotify_search_results

def search(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    search_results = []

    if query:
        search_results = get_spotify_search_results(query)

    return render(request, 'search.html', {
        'search_results': search_results
    })'''

from django.shortcuts import render
from .spotify_helper import get_spotify_search_results

def search(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    search_results = []

    if query:
        search_results = get_spotify_search_results(query)

    return render(request, 'search_results.html', {
        'search_results': search_results,
        'query': query
    })


'''
# recognition/views.py
from django.shortcuts import render, redirect
from .forms import SongUploadForm
from .utils import search_spotify_song

@login_required
def upload_song(request):
    """
    View for uploading the song.
    """
    if request.method == "POST":
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()
            audio_file = song.audio_file
            recognition_result = search_spotify_song(audio_file.name)

            if recognition_result:
                # Store recognition results in session to persist across views
                request.session['song_data'] = recognition_result
                return redirect('show_result')  # Redirect to the result page
    else:
        form = SongUploadForm()

    return render(request, 'upload_song.html', {'form': form})


@login_required
def show_result(request):
    """
    View to display the recognition result.
    """
    song_data = request.session.get('song_data')

    if not song_data:
        # If no result is found, redirect back to upload page
        return redirect('recognition:upload_song')

    return render(request, 'show_result.html', {'song_data': song_data})


'''
# genres

from django.shortcuts import render
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

# Initialize Spotipy with Client Credentials Flow
client_credentials_manager = SpotifyClientCredentials(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# genres/views.py

from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='your_client_id', client_secret='your_client_secret'))

# List of desired genres
desired_genres = [
    "Pop", "Indie", "Love", "Mood", "Party", "Devotional",
    "Hip-Hop", "Dance/Electronic", "Student", "Chill", "Gaming", "K-pop", "Workout",
    "Rock", "Sleep", "Indian Classical", "Instrumental",
    "Metal", "Jazz", "Classical", "Folk & Acoustic", "Focus", "Soul", "Anime"
]

def genre_list(request):
    try:
        # Fetch available categories (genres) from Spotify Browse API
        categories = sp.categories(limit=50)
        genre_list = categories['categories']['items']
        
        # Filter genres to match only the desired ones
        filtered_genres = [genre for genre in genre_list if genre['name'] in desired_genres]

        context = {
            'genres': filtered_genres
        }

        return render(request, 'genre_list.html', context)
    except Exception as e:
        return HttpResponse(f"Error fetching genres: {e}")


def genre_songs(request, genre):
    try:
        # First, we fetch the genre name (from the category list) based on genre ID
        # Fetch available categories (genres) from Spotify Browse API
        categories = sp.categories(limit=50)
        genre_list = categories['categories']['items']
        
        # Find the name of the genre by matching the ID
        genre_name = None
        for item in genre_list:
            if item['id'] == genre:
                genre_name = item['name']
                break

        if genre_name:
            # Now, search for tracks that belong to the genre by name (not ID)
            results = sp.search(q=f'genre:"{genre_name}"', type='track', limit=30)
            tracks = results['tracks']['items']  # Extract tracks from the search results

            if not tracks:
                return HttpResponse(f"No tracks found for genre: {genre_name}")
            
            context = {
                'genre': genre_name,
                'tracks': tracks
            }

            return render(request, 'genre_songs.html', context)
        else:
            return HttpResponse(f"Genre ID '{genre}' not found.")

    except Exception as e:
        return HttpResponse(f"Error fetching tracks for genre {genre}: {e}")

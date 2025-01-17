# myapp/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home Page
    path('about-us/', views.about, name='about'),  # About Us Page
    path('subscription/', views.subscription, name='subscription'), # Subscription
    path('login/', views.login_v, name='login'), # Login
    path('signup/', views.signup, name='signup'), #signup
    path('base/', views.base, name='base'), #base
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('helpcentre/', views.help_center, name="helpcenter"), # Help Center
    path('helpcentre1/', views.help_center1, name="helpcenter"), # Help Center
    path('callback/', views.spotify_callback, name='callback'),
    path('profile/notifications/', views.notifications_view, name='notifications'), 
    path('profilehome/', views.profilehome, name='profile'),
    path('search/', views.search, name='search'),  # New search page
    path('genre/<str:genre>/', views.genre_songs, name='genre_songs'),
    path('genre/', views.genre_list, name='genre_list'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

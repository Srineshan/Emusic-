from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProfileSettings, Notification
from django.utils.text import slugify

@receiver(post_save, sender=ProfileSettings)
def create_profile_update_notification(sender, instance, created, **kwargs):
    if not created:  # Only trigger if it's an update, not a creation
        # Check if any of the fields have changed
        old_profile = ProfileSettings.objects.get(id=instance.id)

        changes = []
        if old_profile.bio != instance.bio:
            changes.append('bio')
        if old_profile.location != instance.location:
            changes.append('location')
        if old_profile.profile_photo != instance.profile_photo:
            changes.append('profile photo')

        if changes:
            # Prepare the message about what changed
            message = f"Your profile was updated. Changed fields: {', '.join(changes)}."
            # Create a new notification
            Notification.objects.create(
                user=instance.user,
                message=message
            )

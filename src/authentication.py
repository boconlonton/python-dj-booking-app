"""Custom authentication backends for the src app."""
from django.contrib.auth.backends import ModelBackend

from .models import Booking


class BookingIDBackend(ModelBackend):
    """
    Custom authentication backend that allows login via email and src ID.
    """
    def authenticate(self, username=None, password=None, **kwargs):
        """Authenticate users.

        Args:
            username (str): specify the username.
            password (str): specify the user password.
        """
        try:
            booking = Booking.objects.get(
                booking_id=password, user__email=username)
        except Booking.DoesNotExist:
            return None
        return booking.user

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.utils import timezone


@receiver(user_signed_up)
def create_tourist_on_signup(request, user, sociallogin=None, **kwargs):
    """Create a Tourist profile automatically when a user signs up (including via social).

    Extracts profile data from social login (Google, etc.) and saves to database.
    For social logins, phone is optional since social providers don't always provide it.
    """
    from .models import Tourist

    # Don't overwrite an existing profile
    if hasattr(user, 'tourist'):
        return

    # Initialize data with basic user info
    phone = ''
    name = user.first_name or user.last_name or user.username
    email = user.email

    # Extract additional data from social login if available
    if sociallogin:
        extra_data = getattr(sociallogin.account, 'extra_data', {}) or {}
        
        # Get name from social provider
        if 'name' in extra_data:
            name = extra_data['name']
        elif 'given_name' in extra_data or 'family_name' in extra_data:
            given = extra_data.get('given_name', '')
            family = extra_data.get('family_name', '')
            name = f"{given} {family}".strip()
        
        # Get phone if available
        phone = extra_data.get('phone') or extra_data.get('phoneNumber') or ''
        
        # Get email if available and not already in user
        if 'email' in extra_data:
            email = extra_data['email']

    # For Google/social signups without phone, we need to make phone nullable in practice
    # Since the model enforces unique=True and phone can't be empty, we'll use a timestamp-based unique identifier
    if not phone:
        # Use a temporary unique identifier based on username and timestamp
        phone = f"google_{user.id}_{timezone.now().timestamp()}"[-10:]

    try:
        Tourist.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone
        )
    except Exception as e:
        # If there's an issue, try creating without phone enforcement
        if "phone" in str(e):
            Tourist.objects.create(
                user=user,
                name=name,
                email=email,
                phone=f"user_{user.id}"  # Fallback unique identifier
            )
        else:
            raise

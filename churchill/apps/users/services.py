import secrets
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _

from churchill.apps.profiles.models import Profile


def create_user(email: str, password: str) -> User:
    user = User(username=email, email=email, is_active=False)
    user.set_password(password)
    user.save()
    Profile.objects.create(user=user)
    return user


def verify_user(verification_token: str) -> bool:
    user = User.objects.get(profile__verification_token=verification_token)
    if user is not None:
        user.is_active = True
        user.save()
        return True
    return False


def send_verification_email(user: User) -> int:
    user.profile.verification_token = secrets.token_urlsafe(16)
    user.profile.save()

    verify_link = f"{settings.BASE_URL}/verify-email/?verification_token={user.profile.verification_token}"
    body = f"Please follow the link to verify you email address {verify_link}"
    message = EmailMultiAlternatives(
        _("Verify your email address"),
        body=body,
        from_email=settings.DEFAULT_EMAIL_FROM,
        to=(user.email,),
    )
    return message.send(fail_silently=False)


def send_reset_password_email(email: str) -> int:
    user = User.objects.filter(email=email).first()
    if user is None:
        return 0

    user.profile.verification_token = secrets.token_urlsafe(16)
    user.profile.save()

    verify_link = f"{settings.BASE_URL}/reset-password/?verification_token={user.profile.verification_token}"
    body = f"Please follow the link to reset your password {verify_link}"
    message = EmailMultiAlternatives(
        _("Reset password request"),
        body=body,
        from_email=settings.DEFAULT_EMAIL_FROM,
        to=(user.email,),
    )
    return message.send(fail_silently=False)


def reset_user_password(verification_token: str, password: str) -> bool:
    user = User.objects.get(profile__verification_token=verification_token)
    if user is not None:
        user.set_password(password)
        user.save()
        return True
    return False

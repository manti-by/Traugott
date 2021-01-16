from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from churchill.apps.users.services import verify_user


@require_http_methods(["GET"])
def verify_email(request):
    verification_token = request.GET.get("verification_token")
    if verify_user(verification_token):
        messages.success(
            request, _("Your email verified successfully, now you can login")
        )
    else:
        messages.warning(request, _("Can't verify you account, please try again"))
    return redirect("index")

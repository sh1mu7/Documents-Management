from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class UserRoles(IntegerChoices):
    ADMIN = 0, _('Admin')
    CLIENT = 1, _('Client')

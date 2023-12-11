from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ApprovalStatus(IntegerChoices):
    PENDING = 0, _('Pending')
    APPROVED = 1, _('Approved')
    ON_PROCESSING = 2, _('On Processing')
    REJECTED = 3, _('Rejected')


class StatusType(IntegerChoices):
    APPROVE = 0, _('Approve')
    REJECT = 1, _('reject')
    PENDING = 2, _('Pending')

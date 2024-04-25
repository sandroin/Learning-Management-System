from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class Status(IntegerChoices):
    lecturer = 1, _("Lecturer")
    student = 2, _("Student")

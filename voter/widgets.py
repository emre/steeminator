from django.forms import ModelForm
from django.db import models

from .models import SteemAccount
from django.forms.widgets import CheckboxInput as DjangoCheckboxInput

class CheckboxInput(DjangoCheckboxInput):
    template_name = "widgets/checkbox.html"
from django.forms import ModelForm
from stashboard.models import Service

class ServiceForm(ModelForm):
    class Meta:
        model = Service




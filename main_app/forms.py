from django.forms import ModelForm
from .models import Timing

class TimingForm(ModelForm):
    class Meta:
        model = Timing
        fields = ('date', 'time_spent')
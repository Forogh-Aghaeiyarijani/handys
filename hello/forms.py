from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Handyman, Booking, Service

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

class HandymanCreationForm(CustomUserCreationForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    zip_code = forms.CharField(max_length=10, required=False)

    # The Meta class should only inherit from CustomUserCreationForm.Meta
    # and should NOT specify 'model = Handyman' or try to add User fields directly.
    class Meta(CustomUserCreationForm.Meta):
        pass # Inherits fields from CustomUserCreationForm.Meta for User model

    def save(self, commit=True):
        user = super().save(commit=False) # This creates the User object
        if commit:
            user.save()
            # Now, create the Handyman object and link it to the newly created User
            handyman = Handyman.objects.create(
                user=user,
                bio=self.cleaned_data.get('bio', ''),
                phone=self.cleaned_data.get('phone', ''),
                address=self.cleaned_data.get('address', ''),
                city=self.cleaned_data.get('city', ''),
                state=self.cleaned_data.get('state', ''),
                zip_code=self.cleaned_data.get('zip_code', ''),
            )
        return user

class BookingForm(forms.ModelForm):
    # We might want to filter handymen and services dynamically later, but for now, show all.
    handyman = forms.ModelChoiceField(queryset=Handyman.objects.all(), empty_label="Select a Handyman")
    service = forms.ModelChoiceField(queryset=Service.objects.all(), empty_label="Select a Service")

    class Meta:
        model = Booking
        fields = ['handyman', 'service', 'date', 'time', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

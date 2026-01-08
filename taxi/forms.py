from django import forms
from django.contrib.auth.forms import UserCreationForm

from taxi.models import Car, Driver


def license_validate(license_number):
    if not (
        len(license_number) == 8
        and license_number[:3].isalpha()
        and license_number[:3].isupper()
        and license_number[3:].isnumeric()
    ):
        raise forms.ValidationError(
            "License number must be in the format XYZ12345"
        )
    return license_number


class DriverCreateForm(UserCreationForm):
    email_address = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = Driver
        fields = UserCreationForm.Meta.fields + (
            "email_address",
            "first_name",
            "last_name",
            "license_number",
        )

    def clean_license_number(self):
        return license_validate(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = (
            "license_number",
        )

    def clean_license_number(self):
        return license_validate(self.cleaned_data["license_number"])


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=Driver.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Car
        fields = (
            "model",
            "manufacturer",
            "drivers",
        )

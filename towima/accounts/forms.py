# Imports
import phonenumbers

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumbers import NumberParseException
from accounts.models import Profile

# This class will create a signup form, from an existing template provided by django.
class SignUpForm(UserCreationForm):

    # All the necessary fields with their attributes (max length, required, etc).
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    #phone_number = forms.CharField(max_length=12)
    date_of_birth = forms.DateField()
    address = forms.CharField(max_length = 50)
    user_types = (('Pharmacist', 'Pharmacist'), ('Customer', 'Customer'))
    user_type = forms.ChoiceField(widget=forms.Select, choices=user_types)

    # This class gives our model metadata. For more info see: https://docs.djangoproject.com/en/dev/topics/db/models/#meta-options.
    class Meta:
        model = User
        fields = (              # The order of the fields.
            'username', 
            'first_name', 
            'last_name', 
            'email',
            'address',
            #'phone_number', 
            'date_of_birth', 
            'user_type', 
            'password1', 
            'password2',
        ) 

    # A custom save function, so that the user data, as well as additional profile data is saved in the database.
    def save(self, commit = True):
        user = super().save(commit=False)
        #phone_number = self.cleaned_data['phone_number']
        date_of_birth = self.cleaned_data['date_of_birth']
        address = self.cleaned_data['address']
        user_type = self.cleaned_data['user_type']
        if commit:
            user.save()
            #profile = Profile(user=user, phone_number=phone_number, date_of_birth=date_of_birth, address=address, user_type=user_type) # Create a new profile.            
            profile = Profile(user=user, date_of_birth=date_of_birth, address=address, user_type=user_type)
            profile.save()  
        return user

# This class will let users edit their profile.
class EditProfileForm(forms.ModelForm):

    # The fields of the form. We only have to define the extra fields from the Profile model, because the other fields are loaded
    # from the User model.
    phone_number = forms.CharField(max_length=12, required=True)
    date_of_birth = forms.DateField(required=True)
    address = forms.CharField(max_length = 50, required=True)

    # If we want to preload the current value in the form of these fields, we need to do it with _init_. The other fields are
    # preloaded in the Meta class by using the User model.
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = self.instance.profile.phone_number
        self.fields['date_of_birth'].initial = self.instance.profile.date_of_birth
        self.fields['address'].initial = self.instance.profile.address

    class Meta:
        model = User
        fields = (
            'username', 
            'first_name', 
            'last_name', 
            'email',
            'address',
            'phone_number', 
            'date_of_birth', 
        )

    # The custom save method. The user model and profile model are saved.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.profile.phone_number = self.cleaned_data['phone_number']
        user.profile.date_of_birth = self.cleaned_data['date_of_birth']
        user.profile.address = self.cleaned_data['address']

        if commit:
            user.save() 
            user.profile.save()

        return user

class VerificationForm(forms.Form):
    country_code = forms.CharField(max_length=3)
    phone_number = forms.CharField(max_length=20)

    def clean_country_code(self):
        country_code = self.cleaned_data['country_code']
        if not country_code.startswith('+'):
            country_code = '+' + country_code
        return country_code

    def clean(self):
        data = self.cleaned_data
        phone_number = data['country_code'] + data['phone_number']
        try:
            phone_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(phone_number):
                self.add_error('phone_number', 'Invalid phone number')
        except NumberParseException as e:
            self.add_error('phone_number', e)


class TokenForm(forms.Form):
    token = forms.CharField(max_length=6)

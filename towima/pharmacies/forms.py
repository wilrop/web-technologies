from django import forms
from pharmacies.models import Pharmacy, Comments

class PharmacyForm(forms.ModelForm):
    name = forms.CharField(max_length = 70)
    phone_number = forms.CharField(max_length=12)
    address = forms.CharField(max_length = 50)
    
    
    class Meta:
        model = Pharmacy
        fields = ('name','address','phone_number')
        widgets = {'slug': forms.HiddenInput()}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def save(self, pk, user, commit = True):
        comment = super().save(commit=False)
        pharmacy = Pharmacy.objects.get(pk = pk)
        comment.pharmacy = pharmacy
        comment.author = user

        if commit:
            comment.save()
        return comment
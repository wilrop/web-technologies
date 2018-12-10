from django import forms
from pharmacists.models import Comments
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def save(self, pk, user, commit = True):
        comment = super().save(commit=False)
        pharmacist_pk = User.objects.get(pk = pk)
        pharmacist = pharmacist_pk.profile
        author = user
        comment.pharmacist = pharmacist
        comment.author = author

        if commit:
            comment.save()
        return comment
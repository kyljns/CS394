from django import forms
from .models import FamilyMember

from django import forms
from .models import FamilyMember


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['user', 'first_name', 'last_name', 'birth_date', 'death_date', 'bio', 'photo', 'parents']

    # Additional customization for parent field (allowing multiple parents)
    parents = forms.ModelMultipleChoiceField(queryset=FamilyMember.objects.all(), required=False)

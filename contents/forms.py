from django import forms
from .models import *


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'name',
            'email',
            'designation',
            'research_interest',
            'level',
            'phone',
            'linked_in',
            'github',
            'google_scholar',
            'photo',
            'about',
            'hidden',
        ]


class SolutionCategoryForm(forms.ModelForm):
    class Meta:
        model = SolutionCategory
        fields = '__all__'


class WhitePaperForm(forms.ModelForm):
    class Meta:
        model = WhitePaper
        fields = '__all__'


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = '__all__'

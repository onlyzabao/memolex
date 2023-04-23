from django import forms
from django.forms import modelformset_factory
from django.core.exceptions import ValidationError
from .models import Word, Package

class PackageCreateForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ["name", "description", "date", "privacy"]
        widgets = {
            "date":forms.DateInput(attrs={"type":"date"})
        }
        required = {
            "date":False
        }

class BaseWordCreateFormSet(forms.BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        words = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            word = form.cleaned_data.get("spelling")
            if word in words:
                raise ValidationError("The word in package is duplicated.")
            words.append(word)

class WordCreateForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["spelling"]

WordCreateFormSet = modelformset_factory(model=Word, form=WordCreateForm, formset=BaseWordCreateFormSet, extra=0, can_delete=True)


import enchant
from django import forms
from .models import Word, Package

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ["name", "description", "date", "privacy"]
        widgets = {
            "date":forms.DateInput(attrs={"type":"date"})
        }
        required = {
            "date":False
        }
        labels = {
            "date":"Review Schedule"
        }

class WordInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        if any(self.errors):
            return
        words = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            dictionary = enchant.Dict("en_US")
            word = form.cleaned_data.get("spelling")
            if not word:
                form.add_error("spelling", "The word field cannot be left blank. Fill out or remove it instead.")
            elif not dictionary.check(word):
                form.add_error("spelling", "This word is spelled incorrectly.")
            elif word.lower() in words:
                form.add_error("spelling", "This word is duplicated.")
            words.append(word)

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["spelling"]
        labels = {
            "spelling":"Word"
        }


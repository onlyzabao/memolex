from django.db.models import Q
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.http import JsonResponse
from .models import Package, Word
from .forms import PackageForm, WordForm, WordInlineFormSet
from .utilities import SpellingTest
import json
import random


# Create your views here.
class PackageListView(LoginRequiredMixin, ListView):
    model = Package
    context_object_name = "packages"
    template_name = "workspace/package_list.html"

    def get_queryset(self):
        base_qs = super(PackageListView, self).get_queryset()
        return base_qs.filter(user=self.request.user)


class PackageDetailView(LoginRequiredMixin, DetailView):
    model = Package
    context_object_name = "package"
    template_name = "workspace/package_detail.html"

    def get_queryset(self):
        base_qs = super(PackageDetailView, self).get_queryset()
        return base_qs.filter(user=self.request.user)


class PackageCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.GET.get("word"):
            extra_forms = 1
            initial_data = [{"spelling": request.GET.get("word")}]
        else:
            extra_forms = 0
            initial_data = []

        WordFormSet = inlineformset_factory(
            parent_model=Package, 
            model=Word, 
            form=WordForm, 
            formset=WordInlineFormSet, 
            extra=extra_forms,
            can_delete=True
        )

        package_form = PackageForm()
        word_formset = WordFormSet(prefix="form", initial=initial_data)

        context = {"package_form":package_form, "word_formset":word_formset}

        return render(request, "workspace/package_form.html", context)
    
    def post(self, request):
        WordFormSet = inlineformset_factory(
            parent_model=Package, 
            model=Word, 
            form=WordForm, 
            formset=WordInlineFormSet, 
            extra=0, 
            can_delete=True
        )

        package_form = PackageForm(data=request.POST)
        word_formset = WordFormSet(data=request.POST, prefix="form")

        if package_form.is_valid() and word_formset.is_valid():
            package = package_form.save(commit=False)
            package.user = request.user
            package.save()
            for word_form in word_formset:
                if not word_form.cleaned_data.get("DELETE", False):
                    word = word_form.save(commit=False)
                    word.package = package
                    word.save()
            return redirect("workspace:package_detail", pk=package.pk)
        else:
            messages.error(request, "Error creating your package.")

            context = {"package_form":package_form, "word_formset":word_formset}

            return render(request, "workspace/package_form.html", context)
        
class PackageUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        package = get_object_or_404(Package, pk=pk)
        WordFormSet = inlineformset_factory(
            parent_model=Package, 
            model=Word, 
            form=WordForm, 
            formset=WordInlineFormSet, 
            extra=0, 
            can_delete=True
        )

        package_form = PackageForm(instance=package)
        word_formset = WordFormSet(instance=package, prefix="form")

        context = {"package_form":package_form, "word_formset":word_formset}

        return render(request, "workspace/package_form.html", context)
    
    def post(self, request, pk):
        package = get_object_or_404(Package, pk=pk)
        WordFormSet = inlineformset_factory(
            parent_model=Package, 
            model=Word, 
            form=WordForm, 
            formset=WordInlineFormSet, 
            extra=0, 
            can_delete=True
        )

        package_form = PackageForm(data=request.POST, instance=package)
        word_formset = WordFormSet(data=request.POST, instance=package, prefix="form")

        if package_form.is_valid() and word_formset.is_valid():
            package_form.save()
            word_formset.save()
            return redirect("workspace:package_detail", pk=package.pk)
        else:
            messages.error(request, "Error updating your package.")

            context = {"package_form":package_form, "word_formset":word_formset}

            return render(request, "workspace/package_form.html", context)
    
class PackageDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        package = get_object_or_404(Package, pk=pk)
        words = Word.objects.filter(package=package)

        words.delete()
        package.delete()

        messages.success(request, "Your package was deleted successfully.")
        return redirect(reverse_lazy("workspace:package_list"))
    
class AddWordView(LoginRequiredMixin, View):
    def post(self, request):
        status = False
        data = json.loads(request.body)

        if "packages_id" in data and "word" in data: 
            spelling = data["word"]
            for package_id in data["packages_id"]:
                duplicated_word = Word.objects.filter(package__id=package_id, spelling=spelling)
                if not duplicated_word.exists():
                    package = Package.objects.get(pk=package_id)
                    word = Word(package=package, spelling=spelling)
                    word.save()
            status = True
    
    
        response = {"success": status}

        return JsonResponse(response)
    
class ReviewSpellingView(LoginRequiredMixin, View):
    def get(self, request, pk):
        words = Word.objects.filter(Q(package__id=pk) & ~Q(progress=100))[:10]

        questions = SpellingTest.generate(words)

        context = {"questions": questions}

        return render(request, "workspace/review_spelling.html", context)
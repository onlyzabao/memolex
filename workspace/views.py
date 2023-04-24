from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package, Word
from .forms import PackageForm, WordFormSet


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
        package_form = PackageForm()
        word_formset = WordFormSet(prefix="form")

        context = {"package_form":package_form, "word_formset":word_formset}

        return render(request, "workspace/package_form.html", context)
    
    def post(self, request):
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
        package_form = PackageForm(instance=package)
        word_formset = WordFormSet(instance=package, prefix="form")

        context = {"package_form":package_form, "word_formset":word_formset}

        return render(request, "workspace/package_form.html", context)
    
    def post(self, request, pk):
        package = get_object_or_404(Package, pk=pk)
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
        
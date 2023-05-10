from random import shuffle
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from community.models import Profile
from .models import Package, Word
from .forms import PackageForm, WordForm, WordInlineFormSet
from .utilities import Test
import json
import math


# Create your views here.
class PackageListView(LoginRequiredMixin, ListView):
    model = Package
    context_object_name = "packages"
    template_name = "workspace/package_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        userID = self.request.GET.get("userID")
        if userID:
            user = get_object_or_404(User, pk=userID)
        else:
            user = get_object_or_404(User, pk=self.request.user.id)

        profile = get_object_or_404(Profile, user=user)

        context["meta"] = {
            "user": user,
            "profile": profile
        }

        return context

    def get_queryset(self):
        base_qs = super(PackageListView, self).get_queryset()
        
        userID = self.request.GET.get("userID")
        if userID:
            base_qs = base_qs.filter(user__id=userID)
            base_qs = base_qs.filter(privacy=True)
        else:
            base_qs = base_qs.filter(user=self.request.user)

        order = self.request.GET.get("order")
        if order == "date" or order == "level":
            base_qs = base_qs.order_by(order)
        
        return base_qs


class PackageDetailView(LoginRequiredMixin, DetailView):
    model = Package
    context_object_name = "package"
    template_name = "workspace/package_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        userID = self.request.GET.get("userID")
        if userID:
            user = get_object_or_404(User, pk=userID)
        else:
            user = get_object_or_404(User, pk=self.request.user.id)

        context["meta"] = {
            "user": user
        }

        return context

    def get_queryset(self):
        base_qs = super(PackageDetailView, self).get_queryset()

        userID = self.request.GET.get("userID")
        if userID:
            base_qs = base_qs.filter(user__id=userID)
            base_qs = base_qs.filter(privacy=True)
        else:
            base_qs = base_qs.filter(user=self.request.user)

        return base_qs


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
    def post(self, request):
        pkList = request.POST.getlist("pk")
        print(pkList)

        for pk in pkList: 
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
            for word in data["word"]: 
                for package_id in data["packages_id"]:
                    duplicated_word = Word.objects.filter(package__id=package_id, spelling=word)
                    if not duplicated_word.exists():
                        package = Package.objects.get(pk=package_id)
                        word = Word(package=package, spelling=word)
                        word.save()
            status = True
    
    
        response = {"success": status}

        return JsonResponse(response)
    
class PackageReviewView(LoginRequiredMixin, View):
    def get(self, request, level, pk):
        words = list(Word.objects.filter(Q(package__id=pk) & ~Q(progress=100))[:10])
        shuffle(words)

        context = {
            "meta": {
                "level": level,
                "package": pk
            }, 
            "words": words
        }

        return render(request, "workspace/review_test.html", context)
    
    def check(request, level, pk):
        questions = request.POST.getlist("questions")
        keys = request.POST.getlist("keys")
        coeffs = request.POST.getlist("coeffs")
        answers = request.POST.getlist("answers")
        
        mark = 0
        testLen = len(questions)        
        results = [False] * testLen

        for i in range(testLen):
            if level == 1:
                answer = answers[i]
                word = Word.objects.get(Q(package__id=pk) & Q(spelling=keys[i]))
            elif level == 2:
                answer = request.POST.get(questions[i])
                answers.append(answer)
                word = Word.objects.get(Q(package__id=pk) & Q(spelling=questions[i]))

            if answer == keys[i]:
                results[i] = True
                mark += 1

                word.progress += math.ceil(100 / int(coeffs[i]))
                if word.progress > 100:
                    word.progress = 100
                word.save()

        score = math.ceil((mark / testLen) * 10)

        return score, mark, list(zip(questions, keys, answers, results))
    
    def update(user, pk, score):
        package = Package.objects.get(id=pk)
        package.update_level()
        
        profile = Profile.objects.get(user__id=user.id)
        profile.update_streak(tested=True)
        profile.update_score(score)
        return
    
    def post(seft, request, level, pk):
        score, mark, test = PackageReviewView.check(request, level, pk)
        PackageReviewView.update(user=request.user, pk=pk, score=score)

        context = {
            "meta": {
                "level": level,
                "package": pk
            },
            "mark": mark,
            "test": test
        }

        return render(request, "workspace/review_result.html", context)
    
class TestGenerateView(LoginRequiredMixin, View):
    def get(self, request):
        level = request.GET.get("level")
        word = request.GET.get("word")
        progress = request.GET.get("progress")

        question = {}
        if level and word and progress:
            question = Test.generate(int(level), word, int(progress))

        context = {
            "question": question
        }

        return JsonResponse(context)
    
class QuestionDisplayView(LoginRequiredMixin, View):
    def get(self, request):
        question = request.GET.get("question")

        if question:
            question = json.loads(question)

        context = {
            "question": question
        }

        return render(request, "workspace/review_question.html", context)
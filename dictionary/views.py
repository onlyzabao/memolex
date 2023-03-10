from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def searching_word(response):
    return HttpResponse('Your word is not found!')
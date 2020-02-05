from django.http import HttpResponse
from django.shortcuts import render

def home(request):
  return render(request, 'homepage.html', {'name':'shounen'})

def about(request):
  return render(request, 'about.html', {})

def game(request):
  return render(request, 'gamepage.html', {})

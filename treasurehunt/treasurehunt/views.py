from django.http import HttpResponse
from django.shortcuts import render
from .game_endpoints import *
# from ...fast_travel import *
# from ...mine import *
# from ...ls8 import *
import os

functions = {
  # "decipher": os.system('python ls8.py well_data.txt'),
  # "mine": os.system('python mine.py'),
  # "move": move(),

}


def base(request):
  return render(request, 'base.html', )

def info(request):
  return render(request, 'info.html',)

def home(request):
  return render(request, 'homepage.html', {})

def about(request):
  return render(request, 'about.html', )

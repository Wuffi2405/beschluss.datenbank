from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
import glob

def index(request):
    return render(request, 'editor.html')
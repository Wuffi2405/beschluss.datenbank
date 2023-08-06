from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import json
import os
import glob
from . import functions as func

def index(request):
    return HttpResponse("Hallo Welt")

#
#   Anzeige eines Beschlusses
#
def view_document(request, document_id=None):
    print("hi")
    if document_id is None:
        return redirect('list_document')
    # check if file exists
    if not os.path.exists(f'./data/{document_id}.json'):
        return render(request, 'viewer/404.html', status=404)
    # read json file from ./data/document_id.json
    document = None
    try:
        document = json.load(open(f'./data/{document_id}.json'))
    except:
        return render(request, 'viewer/500.html', status=500)
    return render(request, 'view_document.html', {'document': document})

#
#   Übersicht über alle Beschlüsse die in unserem System sind
#
def document_overview(request):
    # get all files from ./data
    document_titles = [ f.split('/')[-1].split('.')[0] for f in glob.glob('./data/*.json')]
    
    documents = []
    for p_document in document_titles:   
        documents.append(load_document_json(p_document))
    
    return render(request, 'list_document.html', {'documents': documents})

status = None
#
#   Admin Menü, um verschiedene Operationen auf den JSON-Dateien auszuführen
#
def admin_menu(request):
    global status
    if request.method == "POST":

        if request.POST['option'] == "jSoNnOrMaLiSiErEn":
            status = "fsdfdsfsfsfdsfsfd"
            func.normalize_json()

        return HttpResponseRedirect(reverse('admin_menu'))
    
    return render(request, 'admin_menu.html', {"status": status })

def load_document_json(document_name):
    document = None
    try:
        print(f'./data/{document_name}.json')
        document = json.load(open(f'./data/{document_name}.json'))
    except:
        print("FATAL ERROR: Datei konnte nicht geladen werden")
    return document
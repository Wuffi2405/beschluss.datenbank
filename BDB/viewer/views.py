from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
import glob

def index(request):
    return HttpResponse("Hallo Welt")

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

def list_document(request):
    # get all files from ./data
    document_titles = [ f.split('/')[-1].split('.')[0] for f in glob.glob('./data/*.json')]
    
    documents = []
    for d in document_titles:
        documents.append(load_document(d))
    
    return render(request, 'list_document.html', {'documents': documents})

def load_document(document_name):
    document = None
    try:
        print(f'./data/{document_name}.json')
        document = json.load(open(f'./data/{document_name}.json'))
    except:
        print("FATAL ERROR: Datei konnte nicht geladen werden")
    return document
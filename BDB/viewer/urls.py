from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('documents', list_document, name='list_document'),
    path('document/', view_document, name='cview_document'),
    path('document/<str:document_id>', view_document, name='view_document'),
]
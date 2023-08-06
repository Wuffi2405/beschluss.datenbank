from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path('documents', document_overview, name='list_document'),
    path('document/', view_document, name='cview_document'),
    path('document/<str:document_id>', view_document, name='view_document'),
    path('manage', admin_menu, name='admin_menu'),
]
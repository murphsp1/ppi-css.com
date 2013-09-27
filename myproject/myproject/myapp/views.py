# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm
from myproject.myapp.models import Scores



def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.upload'))
            
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    #score1 = Score

    # Render list page with the documents and the form
    return render_to_response(
        'myapp/upload.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def contact(request):
    return render_to_response('myapp/contact.html')

def search(request):
    return render_to_response('myapp/search.html')

#def upload(request):
#    return render_to_response('myapp/upload.html')

def index(index):
    return render_to_response('myapp/index.html')

def hello_world(request):
    return HttpResponse("<h1>Hello, world.</h1>")    
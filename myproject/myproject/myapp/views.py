# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

import simplejson

from .models import Document
from myproject.myapp.forms import DocumentForm
from .models import Scores
#from .models.zippp.asa import asa
#import myproject.myapp.zippp.molecule.Molecule
#import myproject.myapp.zippp.mu-pot as mu_pot
#from zippp.mu_pot import mu_pot
import zippp.mu_pot as mu_pot
from django.conf import settings


def upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()


            #newscore = Scores(name = 'test', score = 999.1, interface='A:YourMom')
            #newscore.save()
            filename = request.FILES['docfile'].name
            path = settings.MEDIA_ROOT
            file_and_path = path + '/documents/' + filename
            print(file_and_path)
            #asa.main_function(file_and_path)

            score = mu_pot.scoreOne(file_and_path)
            print(score)

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

def index(index):
    return render_to_response('myapp/index.html')

def hello_world(request):
    return HttpResponse("<h1>Hello, world.</h1>")    

#This view simply dumps the current Scores table  
def get_table_data(request):
    # get the objects you wish to return
    scores = Scores.objects.filter()
    # construct a list which will contain all of the data for the response
    to_json = []
    for score in scores:
        to_json.append([score.name, score.interface, "{0:.2f}".format(score.score)])

    # convert the list to JSON
    response_data = simplejson.dumps({"aaData" : to_json})

    # return an HttpResponse with the JSON and the correct MIME type
    return HttpResponse(response_data, mimetype='application/json')

'''
def init_table_data_load(request):
    import csv
    #for remote server
    data_file = open("/home/seanmurphy/myproject/myproject/myproject/myapp/static/csv/energies_merged.csv","rU")
    data_file = open("/Users/seanmurphy/Desktop/ProphecyWebService/django/for_django_1-5/myproject/myproject/myapp/static/csv/energies_merged.csv","rU")
    cr = csv.reader(data_file)
    for row in cr:
        newscore = Scores(name = row[0], score = row[2], interface=row[1])
        newscore.save()

    data_file.close()
    return HttpResponse("<h1>Data Uploaded Successfully</h1>")
'''


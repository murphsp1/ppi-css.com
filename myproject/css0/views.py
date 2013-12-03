# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

import simplejson

from .models import Document
from myproject.css0.forms import DocumentForm
from .models import Scores
import zippp.mu_pot as mu_pot
from django.conf import settings


def upload(request):
    # Handle file upload
    success = False
    error_message = None

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            filename = request.FILES['docfile'].name

            if ( filename[-3:].upper() == 'PDB'):
                newdoc = Document(docfile = request.FILES['docfile'])
                newdoc.save()

                path = settings.MEDIA_ROOT
                file_and_path = path + '/documents/' + filename

                #print(file_and_path)
                try:
                    output_tuple = mu_pot.scoreOne(file_and_path)
                    #print('PDB Name = ' + output_tuple[0])
                    #print('PDB Interface = ' + output_tuple[1])
                    #print('EST DeltaG = '+ str(output_tuple[2]) )
                    newscore = Scores(name = output_tuple[0], score = output_tuple[2], interface=output_tuple[1], uploaded=True)
                    newscore.save()
                    success=True

                except:
                    error_message = "There was an error during the computation, probably due to a problem with the PDB file."

            else:
                error_message = "The file uploaded had the wrong extension."  

                # Redirect to the document list after POST
                #return HttpResponseRedirect(reverse('myproject.css0.views.upload'))
            
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()

    scores = None
    if (success):
        scores = Scores.objects.latest('id')
        scores = [scores]
        print(scores)
    
    # Render list page with the documents and the form
    return render_to_response(
        'css0/upload.html',
        {'scores': scores, 'form': form, 'error_message':error_message},
        context_instance=RequestContext(request)
    )


def contact(request):
    return render_to_response('css0/contact.html')

def search(request):
    return render_to_response('css0/search.html')

def index(index):
    return render_to_response('css0/index.html')
   

#This view simply dumps the current Scores table  
def get_table_data(request):
    # get the objects you wish to return
    scores = Scores.objects.filter()
    # construct a list which will contain all of the data for the response
    to_json = []
    for score in scores:
        if not(score.uploaded):
            to_json.append([score.name, score.interface, "{0:.2f}".format(score.score)])

    # convert the list to JSON
    response_data = simplejson.dumps({"aaData" : to_json})

    # return an HttpResponse with the JSON and the correct MIME type
    return HttpResponse(response_data, mimetype='application/json')


def init_table_data_load(request):
    import csv
    #For production
    data_file = open("/var/www/ppi-css.com/htdocs/static/csv/webpage_DB.csv","rU")
    
    #For development
    #data_file = open("/Users/seanmurphy/Desktop/ProphecyWebService/django/for_django_1-5/myproject/myproject/css0/static/csv/webpage_DB.csv","rU")
    cr = csv.reader(data_file)
    for row in cr:
        print(row[2])
        newscore = Scores(name = row[0], score = float(row[2]), interface=row[1], uploaded=False)
        newscore.save()

    data_file.close()
    return HttpResponse("<h1>Data Uploaded Successfully</h1>")



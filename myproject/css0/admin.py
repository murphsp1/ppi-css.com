from django.contrib import admin
from myproject.css0.models import Scores, Document

class ScoresAdmin(admin.ModelAdmin):
	fields = ('name','score','interface')
	list_display = ('name','score','interface','uploaded')
	list_filter = ('name', 'score')
	search_fields = ['name']
admin.site.register(Scores, ScoresAdmin)



class DocumentAdmin(admin.ModelAdmin):
	list_display = ('docfile','date_uploaded')
admin.site.register(Document, DocumentAdmin)
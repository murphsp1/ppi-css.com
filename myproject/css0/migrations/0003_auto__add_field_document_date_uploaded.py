# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Document.date_uploaded'
        db.add_column(u'css0_document', 'date_uploaded',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 11, 27, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Document.date_uploaded'
        db.delete_column(u'css0_document', 'date_uploaded')


    models = {
        u'css0.document': {
            'Meta': {'object_name': 'Document'},
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 27, 0, 0)'}),
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'css0.scores': {
            'Meta': {'object_name': 'Scores'},
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 11, 27, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'uploaded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['css0']
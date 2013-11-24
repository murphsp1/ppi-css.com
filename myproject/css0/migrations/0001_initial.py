# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'css0_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'css0', ['Document'])

        # Adding model 'Scores'
        db.create_table(u'css0_scores', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('interface', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'css0', ['Scores'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'css0_document')

        # Deleting model 'Scores'
        db.delete_table(u'css0_scores')


    models = {
        u'css0.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'css0.scores': {
            'Meta': {'object_name': 'Scores'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'score': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['css0']
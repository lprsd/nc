# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PdfDownload'
        db.create_table('reg_pdfdownload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phash', self.gf('django.db.models.fields.IntegerField')()),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('reg', ['PdfDownload'])

        # Adding model 'Team'
        db.create_table('reg_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=127, null=True, blank=True)),
            ('store', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('captain_name', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('nregnum', self.gf('django.db.models.fields.IntegerField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal('reg', ['Team'])

        # Adding model 'Player'
        db.create_table('reg_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reg.Team'])),
        ))
        db.send_create_signal('reg', ['Player'])

        # Adding model 'Payment'
        db.create_table('reg_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reg.Team'], null=True, blank=True)),
            ('pdf_download', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reg.PdfDownload'], null=True, blank=True)),
            ('order_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('gateway_ordernum', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('gateway_response', self.gf('django.db.models.fields.CharField')(max_length='10')),
            ('gateway_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('gateway_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('gateway_nbbid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('gateway_formatted_values', self.gf('django.db.models.fields.TextField')()),
            ('gateway_checksum', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('reg', ['Payment'])


    def backwards(self, orm):
        
        # Deleting model 'PdfDownload'
        db.delete_table('reg_pdfdownload')

        # Deleting model 'Team'
        db.delete_table('reg_team')

        # Deleting model 'Player'
        db.delete_table('reg_player')

        # Deleting model 'Payment'
        db.delete_table('reg_payment')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reg.payment': {
            'Meta': {'object_name': 'Payment'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'gateway_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'gateway_checksum': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gateway_formatted_values': ('django.db.models.fields.TextField', [], {}),
            'gateway_nbbid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'gateway_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gateway_ordernum': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'gateway_response': ('django.db.models.fields.CharField', [], {'max_length': "'10'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'pdf_download': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reg.PdfDownload']", 'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reg.Team']", 'null': 'True', 'blank': 'True'})
        },
        'reg.pdfdownload': {
            'Meta': {'object_name': 'PdfDownload'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'phash': ('django.db.models.fields.IntegerField', [], {})
        },
        'reg.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reg.Team']"})
        },
        'reg.team': {
            'Meta': {'object_name': 'Team'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'captain_name': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'nregnum': ('django.db.models.fields.IntegerField', [], {}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['reg']

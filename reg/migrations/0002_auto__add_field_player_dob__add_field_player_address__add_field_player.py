# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Player.dob'
        db.add_column('reg_player', 'dob', self.gf('django.db.models.fields.DateField')(default=datetime.date(2010, 10, 9)), keep_default=False)

        # Adding field 'Player.address'
        db.add_column('reg_player', 'address', self.gf('django.db.models.fields.TextField')(default='Address'), keep_default=False)

        # Adding field 'Player.mobile_phone'
        db.add_column('reg_player', 'mobile_phone', self.gf('django.db.models.fields.IntegerField')(default=11111), keep_default=False)

        # Adding field 'Player.land_phone'
        db.add_column('reg_player', 'land_phone', self.gf('django.db.models.fields.CharField')(default=11111, max_length=10), keep_default=False)

        # Adding field 'Player.emergency_contact'
        db.add_column('reg_player', 'emergency_contact', self.gf('django.db.models.fields.CharField')(default='Nike', max_length=100), keep_default=False)

        # Adding field 'Player.email'
        db.add_column('reg_player', 'email', self.gf('django.db.models.fields.EmailField')(default='mesh@meshach.com', max_length=75), keep_default=False)

        # Adding field 'Player.ailments'
        db.add_column('reg_player', 'ailments', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Player.receive_updates'
        db.add_column('reg_player', 'receive_updates', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'Team.payment_done'
        db.add_column('reg_team', 'payment_done', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Team.payment_detail'
        db.add_column('reg_team', 'payment_detail', self.gf('django.db.models.fields.TextField')(default='None'), keep_default=False)

        # Adding field 'Team.status'
        db.add_column('reg_team', 'status', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Player.dob'
        db.delete_column('reg_player', 'dob')

        # Deleting field 'Player.address'
        db.delete_column('reg_player', 'address')

        # Deleting field 'Player.mobile_phone'
        db.delete_column('reg_player', 'mobile_phone')

        # Deleting field 'Player.land_phone'
        db.delete_column('reg_player', 'land_phone')

        # Deleting field 'Player.emergency_contact'
        db.delete_column('reg_player', 'emergency_contact')

        # Deleting field 'Player.email'
        db.delete_column('reg_player', 'email')

        # Deleting field 'Player.ailments'
        db.delete_column('reg_player', 'ailments')

        # Deleting field 'Player.receive_updates'
        db.delete_column('reg_player', 'receive_updates')

        # Deleting field 'Team.payment_done'
        db.delete_column('reg_team', 'payment_done')

        # Deleting field 'Team.payment_detail'
        db.delete_column('reg_team', 'payment_detail')

        # Deleting field 'Team.status'
        db.delete_column('reg_team', 'status')


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
            'address': ('django.db.models.fields.TextField', [], {}),
            'ailments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'emergency_contact': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_phone': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mobile_phone': ('django.db.models.fields.IntegerField', [], {}),
            'receive_updates': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
            'payment_detail': ('django.db.models.fields.TextField', [], {}),
            'payment_done': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['reg']
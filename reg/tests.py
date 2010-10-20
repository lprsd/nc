"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from nutils.debug import ipython
from django.core.urlresolvers import reverse

class ConvenientTestCase(TestCase):
    def get(self, url_name, *args, **kwargs):
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs))

    def post(self, url_name, *args, **kwargs):
        data = kwargs.pop("data", None)
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data)

    

response3 = {u'Amount': [u'5.00'],
             u'AuthDesc': [u'N'],
             u'Checksum': [u'1171395421'],
             u'Merchant_Id': [u'M_Wizcraft_12245'],
             u'Merchant_Param': [u''],
             u'Notes': [u'aasd'],
             u'Order_Id': [u'30992432:1286221675'],
             u'bank_name': [u''],
             u'billing_cust_address': [u'adasd'],
             u'billing_cust_city': [u'dfasd'],
             u'billing_cust_country': [u'India'],
             u'billing_cust_email': [u'dsafas@sfsdd.ddd'],
             u'billing_cust_name': [u'adasd'],
             u'billing_cust_state': [u'sdfasd'],
             u'billing_cust_tel': [u'23423'],
             u'billing_zip_code': [u'adas'],
             u'card_category': [u'CREDITCARD'],
             u'delivery_cust_address': [u'N/A'],
             u'delivery_cust_city': [u'N/A'],
             u'delivery_cust_country': [u'N/A'],
             u'delivery_cust_name': [u'N/A'],
             u'delivery_cust_state': [u'N/A'],
             u'delivery_cust_tel': [u'N/A'],
             u'delivery_zip_code': [u'N/A'],
             u'nb_bid': [u'234244'],
             u'nb_order_no': [u'CCA101038394'],
             u'return_url': [u'http://smackaho.st/payment-done/']}

from reg.models import Team
class SimpleTest(ConvenientTestCase):
    def setUp(self):
        t = Team()
        t.name = "adasdasd"
        t.address = 'dasdasdas'
        t.store = "LP"
        t.save()
        self.t = t
    #fixtures = ['test_data.json',]
    
    def test_gateway_response(self):
        from time import time
        response3['Order_Id']="%s:%s"%(self.t.nregnum,int(time()))
        my_response = self.post('payment_done',data=response3)
        ipython()
        
    def test_dup_team_name(self):
        pass
    
        
__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}


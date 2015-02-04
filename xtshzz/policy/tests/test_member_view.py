#-*- coding: UTF-8 -*-
import json
import hmac
from hashlib import sha1 as sha
from Products.CMFCore.utils import getToolByName
#from dexterity.membrane.testing import FUNCTIONAL_TESTING

from zope.component import getUtility
from plone.keyring.interfaces import IKeyManager 

from plone.app.testing import TEST_USER_ID, login, TEST_USER_NAME, \
    TEST_USER_PASSWORD, setRoles
from plone.testing.z2 import Browser
import unittest2 as unittest
from plone.namedfile.file import NamedImage
from xtshzz.policy.tests.test_member_listing_view import TestView as base
import os

def getFile(filename):
    """ return contents of the file with the given name """
    filename = os.path.join(os.path.dirname(__file__), filename)
    return open(filename, 'r')

class TestView(base):   

    
    def test_member_view(self):

        app = self.layer['app']
        portal = self.layer['portal']
       
        browser = Browser(app)
        browser.handleErrors = False
        browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
        
        import transaction
        transaction.commit()
        obj = portal['memberfolder']['member1'].absolute_url() + '/view'        

        browser.open(obj)

        outstr = "I am member1"        
        self.assertTrue(outstr in browser.contents)   
        outstr = "qq.com"        
        self.assertTrue(outstr in browser.contents)          

    def test_ajax_member_state(self):
        request = self.layer['request']        
        keyManager = getUtility(IKeyManager)
        secret = keyManager.secret()
        auth = hmac.new(secret,TEST_USER_NAME, sha).hexdigest()
        request.form = {
                        '_authenticator': auth,
                        'state':'pending', #new created member initial status
                        'id':'member1',                                                                       
                        }
        view = self.portal.restrictedTraverse('@@ajaxmemberstate')
        result = view()

        self.assertEqual(json.loads(result),True)         

    def test_member_workflow(self):
        app = self.layer['app']
        portal = self.layer['portal']
        wf = getToolByName(portal, 'portal_workflow')

        wt = wf.dexterity_membrane_workflow
        dummy = portal['memberfolder']['member1']
        wf.notifyCreated(dummy)

        chain = wf.getChainFor(dummy)
        self.failUnless(chain[0] =='dexterity_membrane_workflow')

        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'pending')        
        wf.doActionFor(dummy, 'approve', comment='foo' )

## available variants is actor,action,comments,time, and review_history        
        review_state = wf.getInfoFor(dummy, 'review_state')
        self.assertEqual(review_state,'enabled')
        comment = wf.getInfoFor(dummy, 'comments')
        self.assertEqual(comment,'foo')     
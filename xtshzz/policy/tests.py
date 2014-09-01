#-*- coding: UTF-8  -*-
import unittest2 as unittest
from xtshzz.policy.testing import POLICY_INTEGRATION_TESTING

from Products.CMFCore.utils import getToolByName

class TestSetup(unittest.TestCase):
    
    layer = POLICY_INTEGRATION_TESTING
    
    def test_portal_title(self):
        portal = self.layer['portal']
        self.assertEqual("湘潭社会组织信息网", portal.getProperty('title'))
    
#    def test_portal_description(self):
#        portal = self.layer['portal']
#        self.assertEqual("OWASP中国", portal.getProperty('description'))
#   


#    def test_PloneFormGen_installed(self):
#        portal = self.layer['portal']
#        portal_types = getToolByName(portal, 'portal_types')
#        
#        self.assertTrue("dexterity.membrane.member" in portal_types)
#        self.assertTrue("dexterity.membrane.memberfolder" in portal_types)        
#    
#    def test_diazo960_installed(self):
#        portal = self.layer['portal']
#        portal_types = getToolByName(portal, 'portal_types')
#        
#        self.assertTrue('collective.conference.conference' in portal_types)
#        self.assertTrue('collective.conference.session' in portal_types)        
    
#    def test_metaTypesNotToList_configured(self):
#        portal = self.layer['portal']
#        portal_properties = getToolByName(portal, 'portal_properties')
#        navtree_properties = portal_properties['navtree_properties']
#        metaTypesNotToList = navtree_properties.getProperty('metaTypesNotToList')
#        
#        self.assertTrue("Promotion" in metaTypesNotToList)
#        self.assertTrue("Discussion Item" in metaTypesNotToList)
#        self.assertFalse("Cinema" in metaTypesNotToList)
#    
#    def test_add_promotion_permission_for_staffmember(self):
#        portal = self.layer['portal']
#        
#        self.assertTrue('Optilux: Add Promotion' in [r['name'] for r in 
#                                portal.permissionsOfRole('StaffMember')
#                                if r['selected']])
#    
#    def test_dam_report_installed(self):
#        portal = self.layer['portal']
#        portal_actions = getToolByName(portal, 'portal_actions')
#        
#        self.assertTrue('dam-report' in portal_actions['site_actions'])
#    
#    def test_contact_action_installed(self):
#        portal = self.layer['portal']
#        portal_actions = getToolByName(portal, 'portal_actions')
#        
#        self.assertTrue('enquiry' in portal_actions['site_actions'])
#        self.assertFalse(portal_actions['site_actions']['contact'].visible)
#
#    def test_manage_own_portlets_permission(self):
#        portal = self.layer['portal']
#        
#        self.assertTrue('Portlets: Manage own portlets' in
#                [r['name'] for r in 
#                    portal.permissionsOfRole('StaffMember')
#                        if r['selected']])
#        self.assertFalse('Portlets: Manage own portlets' in
#                [r['name'] for r in 
#                    portal.permissionsOfRole('Member')
#                        if r['selected']])



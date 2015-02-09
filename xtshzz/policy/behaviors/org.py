# -*- coding: utf-8 -*-
from five import grok
from zope.interface import alsoProvides, implements
from zope.interface import Interface
from zope.component import adapts
from zope.component import adapter
from zope.interface import implementer
from zope import schema
from plone.supermodel import model
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
#from plone.namedfile import field as namedfile
from Products.CMFCore.utils import getToolByName

from my315ok.socialorgnization.registrysource import RegistrySource, DynamicVocabulary
from my315ok.socialorgnization.content.orgnization import IOrgnization
from dexterity.membrane.content.member import IOrganizationMember

from xtshzz.policy import MessageFactory as _
class IOrg(Interface):

    def getOrgBn():
        """get relative organization brain
        """
    def getLegalPerson():
        """ 获取法人"""
                               
    def getSponsor():
        """获取监管单位
        """

@implementer(IOrg)
@adapter(IOrganizationMember)
class Org(object):
#    implements(IOrg)
#    adapts(IDexterityContent)
    
    def __init__(self, context):
        self.context = context
        
      
    
    def getOrgBn(self):
        "get sponsor"
        orgid = self.context.orgname
#        import pdb
#        pdb.set_trace()
        if not orgid:return None
        catalog = getToolByName(self.context,"portal_catalog")
        query = {"object_provides":IOrgnization.__identifier__,'id':orgid}

        bs = catalog(query)
        return bs[0]
    
    
    def getOrgPath(self):
        bn = self.getOrgBn()
        if  bn:return bn.getURL()
        return None
    
    def getLegalPerson(self):
        bn = self.getOrgBn()
        if  bn:return bn.orgnization_legalPerson
        return ""
        
        

        
    def getSponsor(self):
        bn = self.getOrgBn()
        if  bn:return bn.orgnization_supervisor
        return ""        


    
    

#class OrgAdapter(grok.Adapter, Org):
#    grok.context(IDexterityContent)
#    grok.implements(IOrg)        
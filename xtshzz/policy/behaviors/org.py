# -*- coding: utf-8 -*-
from five import grok
from zope.interface import alsoProvides, implements
from zope.component import adapts
from zope import schema
from plone.supermodel import model
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
#from plone.namedfile import field as namedfile
from Products.CMFCore.utils import getToolByName

from my315ok.socialorgnization.registrysource import RegistrySource, DynamicVocabulary
from my315ok.socialorgnization.content.orgnization import IOrgnization

from xtshzz.policy import MessageFactory as _
class IOrg(form.Schema):
    
    orgname = schema.Choice(
            title=_(u"organization name"),
            source=DynamicVocabulary("my315ok.socialorgnization.content.orgnization", "IOrgnization")
                        )  
#    orgname = schema.Choice(
#        title=_(u"organization name"),     
#        source=possibleOrganization,     
#        required=True
#    )


alsoProvides(IOrg, IFormFieldProvider)

class Org(object):
#    implements(IOrg)
#    adapts(IDexterityContent)
    
    def __init__(self, context):
        self.context = context
        
    def _get_orgname(self):
        return self.context.orgname

    def _set_orgname(self, value):
        if isinstance(value, str):
            raise ValueError('must be unicode.')
        self.context.orgname = value
    orgname = property(_get_orgname, _set_orgname)        
    
    def getOrgBn(self):
        "get sponsor"
        orgid = self.context.orgname
        catalog = getToolByName(context,"portal_catalog")
        query = {"object_provides":IOrgnization.__identifier__,id:orgid}
        bs = catalog(query)
        return bs[0]
    
    def getLegalPerson(self):
        bn = self.getOrgBn()
        return bn.orgnization_legalPerson
        
    def getSponsor(self):
        bn = self.getOrgBn()
        return bn.orgnization_supervisor
    
    

#class OrgAdapter(grok.Adapter, Org):
#    grok.context(IDexterityContent)
#    grok.implements(IOrg)        
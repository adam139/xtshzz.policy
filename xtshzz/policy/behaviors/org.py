# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.component import adapter
from zope.interface import implementer
from Products.CMFCore.utils import getToolByName

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
    """member adapter"""
    
    def __init__(self, context):
        self.context = context      
    
    def getOrgBn(self):
        "get sponsor"
        orgid = self.context.orgname
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
      
# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.dexterity.utils import createContentInContainer
from my315ok.socialorgnization.content.orgnization import IOrgnization

from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder
from plone.i18n.normalizer.interfaces import INormalizer
from zope.component import getUtility
def init_governmentdepartment(context):
    
    pc = getToolByName(context, "portal_catalog")
    query = {"object_provides":IOrgnizationFolder.__identifier__}
    bns = pc(query)
    folder = bns[0].getObject()
    query = {"object_provides":IOrgnization.__identifier__,"orgnization_belondtoArea":"xiangtanshi"}
    bns = pc(query)

    # create government department data
    title2id = getUtility(INormalizer,'zh')

    ts = [i.orgnization_supervisor for i in bns]

    bsset = set(ts)
    for title in bsset:
        if title == "" or title == None:continue        
        if not isinstance(title, unicode):
            title = unicode(title, 'utf-8')
                    
        # call title to id utility
        id = title2id.normalize(title)
        try:
            item =createContentInContainer(folder,
                                           "my315ok.socialorgnization.governmentorgnization",
                                           checkConstraints=False,
                                           id=id,
                                           title=title)
            item.reindex()
#            setattr(item,'title',title)
        except:
            pass

        
        
    
    
    
    pass


#-*- coding: UTF-8 -*-
from zope.interface import implements
from Acquisition import aq_inner
from zope.dottedname.resolve import resolve
from Products.Five.utilities.marker import mark
from zope.publisher.interfaces import IPublishTraverse
from Products.Five.browser import BrowserView
from zope.interface import Interface
from Products.CMFPlone.interfaces.resources import OVERRIDE_RESOURCE_DIRECTORY_NAME
from zExceptions import NotFound



class setLayout(BrowserView):
    """
    设置指定内容对象的视图名称，通过:contentobj@@set_layout?new_view_name形式来设置。
    """    
    implements(IPublishTraverse)        
    layout = None
    #receive url parameters
    def publishTraverse(self, request, name):

#         import pdb
#         pdb.set_trace()
        if self.layout is None:
            self.layout = name
            return self
        else:
            raise NotFound()
        
    def __call__(self):        
        obj = self.context
        datev = self.request.form.keys()[0]
        try:
            obj.setLayout(datev)
            return "success"
        except:
            return "error"   

class addLink2Collection(setLayout):
    """add link content type to the specify collection.
    通过:collectionobj@@addLink2Collection形式来设置。
    """

   
    def __call__(self):
#         datev = self.layout
        context = self.context
        linkquery = {u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.any', u'v': [u'Link', u'Document']}
        from plone.app.contenttypes.behaviors.collection import ICollection as ICollection_behavior
        query = ICollection_behavior(context).query
#         import pdb
#         pdb.set_trace()
        for qr in query:
            if qr['i'] == 'portal_type':
                break
        if bool(qr):
            query.remove(qr)
            query.append(linkquery)
            
        ICollection_behavior(context).query = query
             


        return "link type has been added to  '%s' successfully ." % (context.Title()) 
    
class setDate(setLayout):
    """set content object create date for dexterity content types.
    通过:contentobj@@set_date?2016-08-08形式来设置。
    """

   
    def __call__(self):
#         datev = self.layout
        datev = self.request.form.keys()[0]
        from datetime import datetime
        context = self.context

        try:
            d= datetime.strptime(datev,'%Y-%m-%d')
        except:
             return "problem with parameter '%s'. usage: @@setdate?YYYY-MM-DD" % datev
        context.setModificationDate(datev)
        context.creation_date = datev
        context.setEffectiveDate(datev)
        context.reindexObject(idxs=['created', 'modified'])

        return "date on '%s' successfully set to %s." % (context.Title(), datev)    

class clearResource (setLayout):
    """ clear TTW customized resources in ZODB
    通过:SITENAME/@@clear_TTWresources形式来嗲。
    """
    def __call__(self):
        from plone.resource.interfaces import IResourceDirectory
        from zope.component import queryUtility
        persistent_directory = queryUtility(IResourceDirectory, name='persistent')
        container = persistent_directory[OVERRIDE_RESOURCE_DIRECTORY_NAME]
#         import pdb
#         pdb.set_trace()
        try:
            static = container['static']
            for res in static.listDirectory():                
                static.__delitem__(res)
            return "remove static resources successful"
        except:        
            return "remove static resources failed"         

class addMarkInterface(setLayout):
    """
    self.layout will be input a name of the mark interface ,this parameter come from browser request url
    # id is yourpackage.interfaces.IFoo.
    usage:http://host/yourobject/@@add_mark?yourpackage.interfaces.Imark
    """
    
    def __call__(self):

        ifid = self.request.form.keys()[0]
        try:
            ifobj = resolve(ifid)
        except:
            return "interface %s can not be resolved" % (ifid)
        context = aq_inner(self.context)
        mark(context,ifobj)        
        return "I has marked %s to provide %s" % (context.id,ifid)        
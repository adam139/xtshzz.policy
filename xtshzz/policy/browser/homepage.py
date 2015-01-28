#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser import BrowserView
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.socialorgnization import _

from my315ok.products.product import Iproduct

from plone.memoize.instance import memoize

fmt = '%Y/%m/%d %H:%M:%S'
import re
from datetime import datetime,timedelta
import socket
import time
import urllib2
try:
    from BeautifulSoup import BeautifulSoup,SoupStrainer
except:
    print "ERROR: could not import BeautifulSoup Python module"
    print
    print "You can download BeautifulSoup from the Python Cheese Shop at"
    print "http://cheeseshop.python.org/pypi/BeautifulSoup/"
    print "or directly from http://www.crummy.com/software/BeautifulSoup/"
    print
    raise
from my315ok.portlet.fetchouterhtml.fetchouterportlet import FetchOutWebPage
from collective.diazotheme.bootstrap.browser.homepage import HomepageView as baseview 

from Products.CMFCore import permissions
from xtshzz.policy.browser.interfaces import IXtshzzThemeSpecific 
grok.templatedir('templates') 


class FrontpageView(baseview):
     
    grok.context(ISiteRoot)
    grok.template('homepage')
    grok.name('index.html')
    grok.layer(IXtshzzThemeSpecific)
    grok.require('zope2.View')      

    
    def carouselid(self):
        return "carouselid"
    
    def active(self,i):
        if i == 0:
            return "active"
        else:
            return ""
        
    @memoize
    def carouselresult(self):
        
        out = """
        <div id="carousel-generic" class="carousel slide">
  <!-- Indicators -->
  <ol class="carousel-indicators">
    <li data-target="#carousel-generic" data-slide-to="0" class="active"></li>
    <li data-target="#carousel-generic" data-slide-to="1"></li>
    <li data-target="#carousel-generic" data-slide-to="2"></li>
  </ol>

  <!-- Wrapper for slides -->
  <div class="carousel-inner">
    <div class="item active">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>
    <div class="item">
      <img src="http://www.xtshzz.org/xinwenzhongxin/tupianxinwen/xiangtanshishekuaizuzhishoucibishuzhanglianxikuaiyishenglizhaokai/@@images/image/preview" alt="..."/>
      <div class="carousel-caption">
        <h3>大会召开</h3>
      </div>
    </div>    
  </div>

  <!-- Controls -->
  <a class="left carousel-control" href="#carousel-generic" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="#carousel-generic" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>

</div>
        """ 
        
        braindata = self.catalog()({'object_provides':Iproduct.__identifier__, 
                                    'b_start':0,
                                    'b_size':3,
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        brainnum = len(braindata)
        if brainnum == 0:return out        

        outhtml = """<div id="%s" class="carousel slide" data-ride="carousel">
        <ol class="carousel-indicators">
        """ % (self.carouselid())
        outhtml2 = '</ol><div class="carousel-inner">'
        for i in range(brainnum):            
            out = """<li data-target='%(carouselid)s' data-slide-to='%(indexnum)s' class='%(active)s'>
            </li>""" % dict(indexnum=str(i),
                    carouselid=''.join(['#',self.carouselid()]),
                    active=self.active(i))
                                               
            outhtml = ''.join([outhtml,out])   # quick concat string
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            outimg = """<div class="%(classes)s">
                        <img src="%(imgsrc)s" alt="%(imgtitle)s"/>
                          <div class="carousel-caption">
                            <h3>%(imgtitle)s</h3>
                              </div>
                                </div>""" % dict(classes=''.join(["item ", self.active(i)]),
                     imgsrc=''.join([objurl, "/@@images/image/preview"]),imgtitle=objtitle)
            outhtml2 = ''.join([outhtml2,outimg])   # quick concat string                    
#        outhtml = outhtml +'</ol><div class="carousel-inner">'
        result = ''.join([outhtml,outhtml2])   # quick concat string
        out = """
        </div><a class="left carousel-control" href="%(carouselid)s" data-slide="prev">
    <span class="glyphicon glyphicon-chevron-left"></span>
  </a>
  <a class="right carousel-control" href="%(carouselid)s" data-slide="next">
    <span class="glyphicon glyphicon-chevron-right"></span>
  </a>
</div>""" % dict(carouselid = ''.join(["#", self.carouselid()]))
        return ''.join([result,out])
                
              
# roll zone


        
    def rollheader(self):
        return u"新闻"
    
    def rollmore(self):
        context = self.getOrgnizationFolder()
        return context.absolute_url()
    
              
        
               
        
# outer html zone


    
    def outhtmlheader(self):
        return u"论坛热帖"
    
    def outhtmlmore(self):
        return "http://plone.315ok.org/"
    
            


    
    def dataparameter(self):
        data = {
                'code':"utf-8",
                'filter':True,
                'target':"http://plone.315ok.org/",
                'tag':"div",
                'cssid':"portal_block_52_content",
                'cssclass':"dxb_bc",
                'attribute':"",
                'regexp':"",
                'index':0,   #fetch first block
                'interval':24
                }
        return data
        
# roll table output
    def getOrgnizationFolder(self):
        from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder
        brains = self.catalog()({'object_provides':IOrgnizationFolder.__identifier__})
        context = brains[0].getObject()
        return context        
        
    def getable(self,view):
        """view: a organization folder object's view name
        call view come from my315ok.socialorgnization orgnization_listing module,
        view name may be "orgnizations_administrative","orgnizations_survey"
        """
        context = self.getOrgnizationFolder()
        fview = getMultiAdapter((context,self.request),name=view)
        # call getMemberList function output table
        return fview.getMemberList()
            

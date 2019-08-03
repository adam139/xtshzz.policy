# -*- coding: UTF-8 -*-
from Acquisition import aq_inner
from dexterity.membrane import _
from dexterity.membrane.content.member import IMember
from my315ok.socialorgnization.content.member import IOrganizationMember
from my315ok.socialorgnization.content.member import ISponsorMember
from my315ok.socialorgnization.content.memberfolder import IMemberfolder
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.memoize.instance import memoize
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from xtshzz.policy.browser.interfaces import IXtshzzThemeSpecific as IThemeSpecific
from zope import event
from zope import schema
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectAddedEvent

import json


grok.templatedir('templates')


class MemberFolderView(grok.View):
    grok.context(IMemberfolder)
    grok.template('member_b3_listing')
    grok.name('admin_view')
    grok.layer(IThemeSpecific)
    grok.require('cmf.ManagePortal')

    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm

    @memoize
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc

    def fullname(self):
        context = self.context
        return context.title

    def tranVoc(self, value, domain="dexterity.membrane",
                target_language="zh_CN"):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(
            self.context, 'translation_service')
        title = translation_service.translate(
            value,
            domain=domain,
            mapping={},
            target_language=target_language,
            context=self.context,
            default="translate")
        return title

    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal, context)

    def _getUserData(self, userId):
        "get user role lists from user id"
        member = self.pm().getMemberById(userId)
        eliminator = ["Authenticated", "Reviewer"]
        roles = [self.tranVoc(role, domain="plone")
                 for role in member.getRoles() if role not in eliminator]
        roles = ','.join(roles)
        return roles

    @memoize
    def allitems(self):
        """fetch all members"""

        memberbrains = self.catalog()(object_provides=IMember.__identifier__,
                                      path="/".join(self.context.getPhysicalPath()),
                                      sort_order="reverse",
                                      sort_on="created")
        return memberbrains

    def getMemberBrains(self, start=0, size=0):
        "return members data"

        if size == 0:
            braindata = self.allitems()
        else:
            braindata = self.catalog()(object_provides=IMember.__identifier__,
                                       path="/".join(self.context.getPhysicalPath()),
                                       sort_order="reverse",
                                       sort_on="created",
                                       b_start=start,
                                       b_size=size)
        return self.outputList(braindata)

    def getOrgFromId(self, Intf, id):
        "search organization through id"

        brains = self.catalog()(object_provides=Intf.__identifier__, id=id)
        if len(brains) == 0:
            return {'url': '#', 'name': u"缺失关联"}
        title = brains[0].Title
        url = brains[0].getURL()
        org = {}
        org['url'] = url
        org['name'] = title
        return org

    def getOrgInfFromBrain(self, brain, orgid):
        "from brain portal_type fetch organization's or government department's interface"

        if brain.portal_type == 'dexterity.membrane.organizationmember':
            exec(
                "from my315ok.socialorgnization.content.orgnization import IOrgnization as Intf")
        else:
            exec("from my315ok.socialorgnization.content.governmentdepartment import IOrgnization as Intf")
        orgNameandUrl = self.getOrgFromId(Intf, orgid)
        return orgNameandUrl

    def getMemberList(self):
        """获取会员列表,this has been stoped"""
        mlist = []
        memberbrains = self.getMemberBrains()

        for brain in memberbrains:
            row = {'id': '', 'name': '', 'type': '', 'url': '', 'roles': '',
                   'email': '', 'register_date': '', 'status': '', 'editurl': '',
                   'delurl': ''}
            row['id'] = brain.id
            row['name'] = brain.Title
            id = brain.getObject().orgname

            if brain.portal_type == 'dexterity.membrane.organizationmember':
                exec(
                    "from my315ok.socialorgnization.content.orgnization import IOrgnization as Intf")

                row['type'] = self.getOrgFromId(Intf, id)
            else:
                exec(
                    "from my315ok.socialorgnization.content.governmentdepartment import IOrgnization as Intf")
                row['type'] = self.getOrgFromId(Intf, id)

            row['url'] = brain.getURL()
            email = brain.email
            row['roles'] = self._getUserData(email)
            row['email'] = email
            row['register_date'] = brain.created.strftime('%Y-%m-%d')
            row['status'] = brain.review_state
            row['editurl'] = row['url'] + '/@@edit-baseinfo'
            row['delurl'] = row['url'] + '/delete_confirmation'
            mlist.append(row)
        return mlist

    def outputList(self, braindata):
        outhtml = ""
        brainnum = len(braindata)
        for i in braindata:
            objurl = i.getURL()
            # member id
            id = i.id
            # relative the member organization id
            orgid = i.getObject().orgname
            name = i.Title
            email = i.email
            roles = self._getUserData(email)
            register_date = i.created.strftime('%Y-%m-%d')
            status = i.review_state
            editurl = "%s/@@edit-baseinfo" % objurl
            delurl = "%s/delete_confirmation" % objurl
            sponsorInf = self.getOrgInfFromBrain(i, orgid)
            sponsor_url = sponsorInf["url"]
            sponsor_name = sponsorInf["name"]

            out = """<tr class="row">
                  <td class="col-md-1">
                      <a href="%(url)s">
                         <span>%(name)s</span>
                      </a>
                  </td>
                  <td class="col-md-2 text-left" >
                      <span>%(roles)s</span>
                  </td>
                  <td class="col-md-3 text-left">
                      <a href="%(sponsor_url)s">
                         <span>%(sponsor_name)s</span>
                      </a>
                  </td>
                  <td class="col-md-2 text-left">%(email)s
                  </td>
                  <td class="col-md-1">%(register_date)s
                  </td>
                  <td class="col-md-1 handler">""" % dict(url=objurl,
                                                          name=name,
                                                          roles=roles,
                                                          sponsor_url=sponsor_url,
                                                          sponsor_name=sponsor_name,
                                                          email=email,
                                                          register_date=register_date)

            if status == "enabled":
                out1 = """
                    <input type="checkbox"
                                  id="%(id)s"
                                  data-state=%(status)s
                                  class="iphone-style-checkbox hidden"
                                  checked="checked"/>
                                  <span rel="%(id)s" class="iphone-style on">&nbsp;</span>""" % dict(id=id, status=status)
            elif status == "disabled" or status == "pending":
                out1 = """
                    <input type="checkbox"
                        id="%(id)s"
                        data-state=%(status)s
                        class="iphone-style-checkbox hidden" />
                        <span rel="%(id)s" class="iphone-style off">&nbsp;</span>""" % dict(id=id, status=status)
            out2 = """</td>
                  <td class="col-md-2">
                                    <div i18n:domain="plone" class="row">
                                        <div class="col-md-6 text-center">
                                        <a href="%(editurl)s" class="link-overlay btn btn-success">
                                      <i class="icon-pencil icon-white"></i>编辑</a>
                                  </div>
                                  <div class="col-md-6 text-center">
                                          <a href="%(delurl)s" class="link-overlay btn btn-danger">
                                      <i class="icon-trash icon-white"></i>删除</a>
                                  </div>
                                    </div>
                   </td>
                  </tr>""" % dict(editurl=editurl, delurl=delurl)
            outhtml = "%s%s%s%s" % (outhtml, out, out1, out2)
        return outhtml

    def pendingDefault(self, size=10):
        "计算缺省情况下，还剩多少条"
        total = len(self.allitems())
        if total > size:
            return total - size
        else:
            return 0

    def search_multicondition(self, query):
        return self.catalog()(query)


class MemberAjaxSearch(grok.View):
    """AJAX action for search.
    """

    grok.name('member_ajax')
    grok.context(IMemberfolder)
    grok.layer(IThemeSpecific)
    grok.require('cmf.ManagePortal')

    def render(self):
        searchview = getMultiAdapter(
            (self.context, self.request), name=u"admin_view")
        datadic = self.request.form
        start = int(datadic['start'])  # batch search start position
        size = int(datadic['size'])      # batch search size
        # search all
        totalbrains = searchview.allitems()
        totalnum = len(totalbrains)
        # batch search
        outhtml = searchview.getMemberBrains(start=start, size=size)
        data = self.output(start, size, totalnum, outhtml)
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)

    def output(self, start, size, totalnum, outhtml):
        "根据参数total,braindata,返回jason 输出"
        data = {
            'searchresult': outhtml,
            'start': start,
            'size': size,
            'total': totalnum}
        return data


class MemberMore(grok.View):
    """member list view AJAX action for click more. default batch size is 10.
    """

    grok.context(IMemberfolder)
    grok.name('membermore')
    grok.require('zope2.View')

    def render(self):
        form = self.request.form
        formst = form['formstart']
        formstart = int(formst) * 10
        nextstart = formstart + 10
        more_view = getMultiAdapter(
            (self.context, self.request), name=u"admin_view")
        favoritenum = len(more_view.allitems())

        if nextstart >= favoritenum:
            ifmore = 1
            pending = 0
        else:
            ifmore = 0
            pending = favoritenum - nextstart

        pending = "%s" % (pending)
        outhtml = more_view.getMemberBrains(formstart, 10)
        data = {'outhtml': outhtml, 'pending': pending, 'ifmore': ifmore}

        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)


class MemberFolderB3View(MemberFolderView):
    grok.context(IMemberfolder)
#    grok.template('member_b3_listing')
    grok.template('member_ajax_listings_b3')
    grok.name('adminb3_view')
    grok.layer(IThemeSpecific)
    grok.require('cmf.ManagePortal')


class memberstate(grok.View):
    "receive front ajax data,change member workflow status"
    grok.context(IMemberfolder)
    grok.name('ajaxmemberstate')
    grok.layer(IThemeSpecific)
    grok.require('zope2.View')

    def render(self):
        data = self.request.form
        id = data['id']
        state = data['state']
        catalog = getToolByName(self.context, 'portal_catalog')
        obj = catalog({'object_provides': IMember.__identifier__,
                       'path': "/".join(self.context.getPhysicalPath()),
                       "id": id})[0].getObject()
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        registration = getToolByName(self.context, 'portal_registration')
# obj current status
        if state == "pending":  # this is a new account
            try:
                portal_workflow.doActionFor(obj, 'approve')
                try:
                    response = registration.registeredNotify(obj.email)
                except BaseException:
                    raise
                # is sponsor member?  send event update relative government
                # department update operator
                if ISponsorMember.providedBy(obj):
                    event.notify(ObjectAddedEvent(obj, self.context, obj.id))
                result = True
            except BaseException:
                result = False
        elif state == "disabled":
            try:
                portal_workflow.doActionFor(obj, 'enable')
                result = True
            except BaseException:
                result = False
        else:
            try:
                portal_workflow.doActionFor(obj, 'disable')
                # to do remove the account form government department's
                # operators list
                result = True
            except BaseException:
                result = False
        obj.reindexObject()
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(result)

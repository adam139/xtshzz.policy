#-*- coding: UTF-8 -*-
from plone.app.layout.viewlets.content import WorkflowHistoryViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
class ReviewViewlet(WorkflowHistoryViewlet):
    render = ViewPageTemplateFile("templates/review_history.pt")
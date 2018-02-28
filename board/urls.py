from django.conf.urls import url
from django.views.generic.base import TemplateView


from . import views

app_name = 'board'
urlpatterns = [
	url(r'^$', views.home),
	url(r'^viewWork/$', views.viewWork),
	url(r'^DoWriteBoard/$', views.DoWriteBoard),
	url(r'^writeBoard/$', views.writeBoard),
	url(r'^DeleteSpecificRow/$', views.DeleteSpecificRow),
	url(r'^ModifyRow/$', views.ModifyRow),
	url(r'^updateBoard/$', views.updateBoard), 
	url(r'^page_move/$', views.page_move),
	url(r'^DoWriteReply/$', views.DoWriteReply),
	url(r'^DeleteReply/$', views.DeleteReply),
	url(r'^passCheck/$', views.passCheck),
]
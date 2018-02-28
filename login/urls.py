from django.conf.urls import url
from django.views.generic.base import TemplateView


from . import views

app_name = 'login'
urlpatterns = [
	url(r'^$', TemplateView.as_view(template_name='login/index.html'), name='index'),
]
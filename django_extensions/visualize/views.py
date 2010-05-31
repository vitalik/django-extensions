from StringIO import StringIO
from django import forms
from django.http import HttpResponse
from django.conf import settings
from django.db.models.loading import get_apps
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.template.context import RequestContext
from django_extensions.visualize import output
from django_extensions.visualize.modelviz import generate_dot

def _appname(app):
    return app.__name__.split('.')[-2]

APP_CHOICES = [(_appname(app),_appname(app)) for app in get_apps()]


class AppsForm(forms.Form):
    a = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), 
                                  label='applications',
                                  choices=APP_CHOICES, required=False)
    

def _image(request):
    apps = request.GET.getlist('a')
    dotdata = generate_dot(apps)
    stream = StringIO()
    output(stream, dotdata, layout='dot', format='png')
    stream.buf = ''
    return HttpResponse(stream.getvalue(), 'image/png')

def _form(request):
    form = AppsForm(request.GET)
    return render_to_response('django_extensions/graph_models.html'
                       , {'form':form, 'request': request}, 
                       RequestContext(request))

def graph_models(request):
    if 'image' in request.GET:
        return _image(request)
    return _form(request)

if not getattr(settings, 'EXTENSIONS_MODELVIZ_NO_ADMIN', False):
    graph_models = staff_member_required(graph_models)

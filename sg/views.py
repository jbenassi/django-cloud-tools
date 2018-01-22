from django.shortcuts import render

# Create your views here.
from django.template import loader
from django.http import HttpResponse
import boto3
from django.views.generic import TemplateView


def index(request):
    context = {}
    template = loader.get_template('aws_admin/sg_list.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('aws_admin/' + load_template)
    return HttpResponse(template.render(context, request))


class SG(object):
    def get_all(self):
        ec2 = boto3.client('ec2')
        thissession = boto3.session.Session()
        sgs = ec2.describe_security_groups()
        thisregion = thissession.region_name
        thisprofile = thissession.profile_name
        sgs["region"] = thisregion
        sgs["profile"] = thisprofile
        return sgs


class sg_list(TemplateView):
    template_name = 'aws_admin/sg_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sgs'] = SG.get_all(self)
        return context




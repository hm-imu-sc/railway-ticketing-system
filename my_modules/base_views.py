import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway_ticketing_system.settings')
import django
django.setup()

from django.shortcuts import render, redirect

# Create your views here.

class View:

    def respond(self, request, *args, **kwargs):
        pass

    @classmethod
    def as_view(cls, login_required=False, logout_required=False):
        return cls().respond

class TemplateContextView(View):

    def get_template(self):
        pass

    def get_context(self, request, *args, **kwargs):
        return {}

    def respond(self, request, *args, **kwargs):
        return render(request, template_name=self.get_template(), context=self.get_context(request, args, kwargs))

class NoTemplateView(View):

    def act(self, request, *args, **kwargs):
        pass

    def get_redirection(self):
        pass

    def respond(self, request, *args, **kwargs):
        self.act(request, args, kwargs)
        return redirect(self.get_redirection())
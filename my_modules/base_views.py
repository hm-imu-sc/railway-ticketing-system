import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway_ticketing_system.settings')
import django
django.setup()

from django.shortcuts import render, redirect

# Create your views here.

class View:
    login_required = False
    logout_required = False

    def respond(self, request, *args, **kwargs):

        user = {'login_status': False}

        try:
            user = request.session['user']
        except KeyError:
            request.session['user'] = user

        if (self.login_required and user['login_status']) or (self.logout_required and not user['login_status']):
            return self._get_requested_response(request, args, kwargs)
        elif self.login_required:
            return redirect('main:login_page')
        elif self.logout_required:
            return redirect('main:home_page')
        else:
            return self._get_requested_response(request, args, kwargs)

    def _get_requested_response(self, request, *args, **kwargs):
        pass

    @classmethod
    def as_view(cls, login_required=False, logout_required=False):
        cls.login_required = login_required
        cls.logout_required = logout_required
        return cls().respond

class TemplateContextView(View):

    def get_template(self):
        pass

    def get_context(self, request, *args, **kwargs):
        return {}

    def _get_requested_response(self, request, *args, **kwargs):
        return render(request, template_name=self.get_template(), context= {
            **self.get_context(request, args, kwargs),
            'session': dict(request.session)
        })

class NoTemplateView(View):

    def act(self, request, *args, **kwargs):
        pass

    def get_redirection(self):
        pass

    def _get_requested_response(self, request, *args, **kwargs):
        self.act(request, args, kwargs)
        return redirect(self.get_redirection())
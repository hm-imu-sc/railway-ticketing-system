
from my_modules.base_views import TemplateContextView, NoTemplateView

class Home(TemplateContextView):
    def get_template(self):
        return 'home_page.html'

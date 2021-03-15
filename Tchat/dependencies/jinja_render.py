from jinja2 import Environment, PackageLoader, select_autoescape
from nameko.extensions import DependencyProvider

class TemplateRenderer():
     def __init__(self, package_name, directory) -> None:
         self.template_environment = Environment(loader=PackageLoader(package_name, directory),autoescape=select_autoescape(['html']))
     
     def render_homepage(self, messages):
          template = self.template_environment.get_template('home.html')
          return template.render(messages=messages)
     
class Jinja2(DependencyProvider):
     def setup(self):
          self.template_renderer = TemplateRenderer('Tchat', 'templates')
     
     def get_dependency(self, worker_ctx):
          return self.template_renderer
          
from typing import Any
import jinja2
from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http
from redis import RedisError
from werkzeug.wrappers import Response

from .dependencies.redis_client import  MessageStore
from .dependencies.jinja_render import TemplateRenderer, Jinja2
import json



class MessageService:
     name = 'message_service'
     message_store = MessageStore()
     
     @rpc
     def get_message(self, message_id):
     
          return self.message_store.get_message(message_id)

     @rpc 
     def save_message(self, message):
         return self.message_store.save_message(message)
     
     @rpc
     def get_all_messages(self):
          return self.message_store.get_all_messages()


class WebServer:
     name = 'web_server'
     message_service = RpcProxy('message_service')
     templates = Jinja2()


     @http('GET', '/')
     def home(self, request):
          messages = self.message_service.get_all_messages()
          rendered_template = self.templates.render_homepage(messages)
          html_response = create_html_response(rendered_template)

          return html_response
     
     @http('POST','/post')
     def post_message(self, request):
          data_text = request.get_data(as_text=True)

          try:
               data = json.loads(data_text)

          except json.JSONDecodeError:
               return 400, 'JSON Payload expected'

          try:
               message = data.get('message')

          except KeyError:
               return 400, 'No Message given!'
          
          self.message_service.save_message(message) if message != None else 'No Message available'

          return 204, ''


def create_html_response(content):
     headers = {'Content-Type': 'text/html'}
     return Response(content, status=200, headers=headers)




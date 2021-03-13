from nameko.rpc import rpc, RpcProxy
from nameko.web.handlers import http


from .dependencies.redis_client import  MessageStore


class MessageService:
     name = 'message_service'
     message_store = MessageStore()
     
     @rpc
     def get_message(self, message_id):
          return self.message_store.get_message(message_id)


class WebServer:
     name = 'web_server'
     konichwa_service = RpcProxy('konichwa_service')

     @http('GET', '/')
     def home(self, request):
          return self.konichwa_service.konichwa()


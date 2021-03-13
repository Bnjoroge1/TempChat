from redis import  RedisError, StrictRedis
from nameko.extensions import DependencyProvider



class RedisClient:
     def __init__(self, url) -> object:
         self.redis = StrictRedis.from_url(url, decode_responses=True)

     
     def get_message(self, message_id):
          message = self.redis.get(message_id)

          if message is None:
               return RedisError(f'Message Not Found!{message_id}')
          return message

class MessageStore(DependencyProvider):
     def setup(self):
          redis_url = self.container.config['REDIS_URL']
          self.client = RedisClient(redis_url)

     def stop(self):
          return self.client

     def get_dependency(self, worker_ctx):
          return self.client

class RedisError(Exception):
     pass
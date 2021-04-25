from nameko.rpc import rpc

from .dependencies.users import  UserStore, Base
from sqlalchemy.exc import IntegrityError

class UserService:
     name = 'user_service'
     user_store = UserStore(Base)

     @rpc
     def create_user(self, first_name, last_name, email, password):
          self.user_store.create(first_name=first_name,last_name=last_name,email=email, password=password)







from sqlalchemy import Column, Integer, Unicode, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound 

from nameko_sqlalchemy import DatabaseSession
import bcrypt


Base = declarative_base()
HASH_WORK_FACTOR = 15


def hash_password(plain_text_password):
     salt = bcrypt.gensalt(rounds=HASH_WORK_FACTOR)
     encoded_password = plain_text_password.encode()
     return bcrypt.hashpw(encoded_password, salt)

class User(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True)
     first_name = Column(Unicode(length=128))
     last_name = Column(Unicode(length=128))
     email = Column(Unicode(length=128))
     password = Column(LargeBinary())


class UserWrapper:
     def __init__(self, session) -> None:
              self.session = session

     def create_user(self,**kwargs):
          unhashed_pwd = kwargs.get('password')
          hashed_password = hash_password(unhashed_pwd)
          kwargs.update(hashed_password)
          
          user = User(**kwargs)
          self.session.add(user)

          try:
               self.session.commit() 
          except IntegrityError as err:
               self.session.rollback() 
               error_message = err.args[0] 
     
               if 'already exists' in error_message:
                    email = kwargs.get('email')
                    message = f'User already exists - {email}'

                    raise DuplicateUserError(message) 
               else:
                    raise CreateUserError(error_message) 
     def get_user(self, email):
          query = self.session.query(User)

          try:
               user = query.filter_by(email=email).one()
          
          except NoResultFound:
               message = f'User Not Found - {email}'
               raise NoUserFoundError(message)
          
          return user
     

                    


class CreateUserError(Exception):
     pass

class DuplicateUserError(CreateUserError):
     pass

class NoUserFoundError(Exception):
     pass

class UserStore(DatabaseSession):

     def __init_(self):
          super().__init__(Base)


     def get_dependency(self, worker_ctx):
         db_session = super().get_dependency(worker_ctx)
         return UserWrapper(session=db_session)



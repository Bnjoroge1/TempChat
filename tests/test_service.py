from nameko.testing.services import worker_factory
from Tchat.service import MessageService

def test_get_message():
     service_fac = worker_factory(MessageService)
     result = service_fac.get_message('hello')
     assert result == 'msg'

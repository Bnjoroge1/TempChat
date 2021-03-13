from nameko.testing.services import worker_factory
from Tchat.service import KonichwaServ

def test_konichwa():
     service_fac = worker_factory(KonichwaServ)
     result = service_fac.konichwa()
     assert result == 'Konichwa!'

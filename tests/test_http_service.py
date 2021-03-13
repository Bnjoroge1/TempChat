from Tchat.service import KonichwaServ, WebServer

def test_root_http(web_session, web_config, container_factory):
     web_config['AMQP_URI'] = 'pyamqp://guest:guest@localhost'
     web_server = container_factory(WebServer, web_config)
     konichwa = container_factory(KonichwaServ, web_config)
     web_server.start()
     konichwa.start()
     
     result = web_session.get('/')

     assert result.text == 'Konichwa!'

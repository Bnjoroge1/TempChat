from Tchat.service import MessageService, WebServer

def test_root_http(web_session, web_config, container_factory):
    
     web_server = container_factory(WebServer, web_config)
     msg_serv = container_factory(MessageService, web_config)
     web_server.start()
     msg_serv.start()
     
     result = web_session.get('/')

     assert isinstance(result, dict)
     assert result.get('hello') == 'msg'

# def test_post_message(web_session, web_config, container_factory):
#      web_config['AMQP_URI'] = 'pyamqp://guest:guest@localhost'
#      web_server = container_factory(WebServer, web_config)
#      message_serv = container_factory(MessageService, web_config)

#      web_server.start()
#      message_serv.start()

#      result = web_session.post('/post', )


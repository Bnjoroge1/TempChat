from flask import Flask, render_template, request
from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from flask.json import jsonify
import yaml
import os

config_file = os.path.abspath(os.path.dirname('TempChat'))
config_path = os.path.join(config_file, 'config.yaml')                                              
with open('config.yaml', 'r') as config_f:
     config = yaml.load(config_f)
with open('web_config.yaml', 'r') as config_f:
     web_config = yaml.load(config_f)    
app = Flask(__name__)


class  MessageAPI(MethodView):
     def get(self):
          with ClusterRpcProxy(config) as rpc_config:
               messages = rpc_config.message_service.get_all_messages()
     
          return jsonify(messages)
     def post(self):
          data =  request.get_json(force=True)
          
          try:
               message = data['message']
          except KeyError:
               return 'No Message given'
     
          with ClusterRpcProxy(config) as rpc:
               rpc.message_service.sve_message(message)
                       

@app.route('/')
def home():
     return render_template('home.html')


app.add_url_rule(
'/messages', view_func=MessageAPI.as_view('messages')
)                                                 app.secret_key = web_config['FLASK_SECRET_KEY']
app.run()
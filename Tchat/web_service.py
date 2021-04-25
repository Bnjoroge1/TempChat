from nameko.exceptions import RemoteError
from flask import Flask, render_template, request, session, redirect, url_for
from flask.views import MethodView
from nameko.standalone.rpc import ClusterRpcProxy
from flask.json import jsonify
import yaml
import os

config_file = os.path.abspath('Tchat/web_config.yaml')
                                             
with open('config.yaml', 'r') as config_f:
     config = yaml.load(config_f)
     
with open(config_file, 'r') as config_f:
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
               
class SignUpView(MethodView):
     def get(self):
          return render_template('sign_up.html')
     
     def post(self):
          first_name = request.form.get('first_name')
          last_name = request.form.get('last_name')
          email = request.form.get('email')
          password = request.form.get('password')
          
          with ClusterRpcProxy(config) as web_rpc:
               try:
                    web_rpc.user_service.create_user(first_name=first_name, last_name=last_name,email=email, password=password)
               except RemoteError as remote_err:
                    message = f'Unable to Create User{remote_err}'
                    app.logger.error(message)
                    return render_template('sign_up.html', error_msg =message)
          
          session['authenticated']  = True
          session['email'] = email
          
          return redirect(url_for('home'))
          
                       
                  
          

@app.route('/')
def home():
     return render_template('home.html')


app.add_url_rule(
'/messages', view_func=MessageAPI.as_view('messages')
)    

app.add_url_rule(
'/sign_up', view_func=SignUpView.as_view('sign_up')
)    

app.secret_key = web_config['FLASK_SECRET_KEY']
app.run()
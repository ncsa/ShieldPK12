from flask import Flask, session, render_template, request, g, abort, redirect, url_for
from flask_login import (
     LoginManager,
     login_user,
     login_required,
     logout_user,
     current_user
)
from oic import rndstr
from oic.oic import Client
from oic.oic.message import AuthorizationResponse, RegistrationResponse, ClaimsRequest, Claims
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.utils.http_util import Redirect

from qirapi_connection import update_test_status
from access_control_connection import lookup_access_status, update_access_status
from logging_custom_message import logging_custom_message
from tncapi_connection import lookup_name
from user import User

app = Flask(__name__)

# OIDC setting
app.config.from_pyfile('config.py', silent=True)

# set secret key for session
app.secret_key = app.config["CUPHD_SECRET_KEY"]

# create oidc client
client = Client(client_authn_method=CLIENT_AUTHN_METHOD)

# get authentication provider details by hitting the issuer URL
provider_info = client.provider_config(app.config["ISSUER_URL"])

# store registration details
info = {
     "client_id": app.config["CLIENT_ID"],
     "client_secret": app.config["CLIENT_SECRET"],
     "redirect_uris": app.config["REDIRECT_URIS"]
}
client_reg = RegistrationResponse(**info)
client.store_registration_info(client_reg)
client.redirect_uris = app.config["REDIRECT_URIS"]

# LOGIN management setting
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(netid):
     return User.get(netid)


@app.route('/login')
def login():
     session['state'] = rndstr()
     session['nonce'] = rndstr()

     # setup claim request
     claims_request = ClaimsRequest(
          userinfo = Claims(uiucedu_uin={"essential": True})
     )

     args = {
          "client_id": client.client_id,
          "response_type": "code",
          "scope": app.config["SCOPES"],
          "nonce": session["nonce"],
          "redirect_uri": app.config["REDIRECT_URIS"][0],
          "state":session["state"],
          "claims":claims_request
     }

     auth_req = client.construct_AuthorizationRequest(request_args=args)
     login_url = auth_req.request(client.authorization_endpoint)

     return Redirect(login_url)


@app.route('/callback')
def callback():
     response = request.environ["QUERY_STRING"]

     authentication_response = client.parse_response(AuthorizationResponse, info=response, sformat="urlencoded")
     code = authentication_response["code"]

     assert authentication_response["state"] == session["state"]

     args = {
          "code": code
     }

     token_response = client.do_access_token_request(state=authentication_response["state"], request_args=args,
                                                     authn_method="client_secret_basic")

     user_info = client.do_user_info_request(state=authentication_response["state"])
     if "uiucedu_is_member_of" in user_info.keys() and app.config["ROLE"] in user_info["uiucedu_is_member_of"]:
          user = User(netid=user_info["preferred_username"])
          login_user(user)
          logging_custom_message(
              {"message": f"Login user: {user_info['preferred_username']}"})

          return redirect(url_for("homepage"))
     else:
          abort(403, "This is an CUPHD administrator only tool. Your NETID need to be preapproved!")


@app.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect(app.config["ISSUER_URL"] + "/idp/profile/Logout")

@app.route('/', methods=['GET'])
def homepage():
     if current_user.is_authenticated:
          user = current_user.display_name
          return render_template('homepage.html', user=user)
     else:
          return redirect(url_for("login"))


@app.route('/search', methods=['POST'])
def search():
     if current_user.is_authenticated:
          if request.get_json() and request.get_json()['uin']:
               uin = request.get_json()['uin']
               access_status, access_data = lookup_access_status(uin)
               username_status, username_data = lookup_name(uin)
               logging_custom_message(message="User name found at TNC: %s" % username_data)
               if not access_status:
                    abort(500, 'Access API - ' + access_data['message'])
               elif not username_status:
                    abort(500, 'TNC API - ' + username_data['message'])
               else:
                    user_status_obj = {
                         "uin": access_data['data']["uin"],
                         "given_name": username_data['data']['firstName'],
                         "family_name": username_data['data']['lastName'],
                         "status": access_data['data']["allowAccess"]
                    }
                    return {"user": user_status_obj}
          else:
               abort(400, 'UIN is a required field!')
     else:
          abort(403, 'User not Authorized! Please login first.')


@app.route('/quarantine', methods=['POST'])
def quarantine():
     if current_user.is_authenticated:
          if request.get_json() and request.get_json()['uin']:
               uin = request.get_json()['uin']
               access_control_status, access_control_data = update_access_status(uin=uin, allowAccess=False)
               username_status, username_data = lookup_name(uin)
               qir_status, qir_data = update_test_status(uin=uin, test_status="quarantine")
               if not qir_status:
                    abort(500, 'QIR API - ' + qir_data['message'])
               elif not access_control_status:
                    abort(500, 'Access API - ' + access_control_data['message'])
               elif not username_status:
                    abort(500, 'TNC API - ' + username_data['message'])
               else:
                    user_status_obj = {
                         "uin": uin,
                         "given_name": username_data['data']['firstName'],
                         "family_name": username_data['data']['lastName'],
                         "status": access_control_data['data']["allowAccess"]
                    }
                    return {
                         "user": user_status_obj
                    }

          else:
               abort(400, 'UIN is a required field!')
     else:
          abort(403, 'User not Authorized! Please login first.')


@app.route('/isolate', methods=['POST'])
def isolate():
     if current_user.is_authenticated:
          if request.get_json() and request.get_json()['uin']:
               uin = request.get_json()['uin']
               access_control_status, access_control_data = update_access_status(uin=uin, allowAccess=False)
               username_status, username_data = lookup_name(uin)
               qir_status, qir_data = update_test_status(uin=uin, test_status="isolate")
               if not qir_status:
                    abort(500, 'QIR API - ' + qir_data['message'])
               elif not access_control_status:
                    abort(500, 'Access API - ' + access_control_data['message'])
               elif not username_status:
                    abort(500, 'TNC API - ' + username_data['message'])
               else:
                    user_status_obj = {
                         "uin": uin,
                         "given_name": username_data['data']['firstName'],
                         "family_name": username_data['data']['lastName'],
                         "status": access_control_data['data']["allowAccess"]
                    }
                    return {
                         "user": user_status_obj
                    }
          else:
               abort(400, 'UIN is a required field!')
     else:
          abort(403, 'User not Authorized! Please login first.')


@app.route('/release', methods=['POST'])
def release():
     if current_user.is_authenticated:

          if request.get_json() and request.get_json()['uin']:
               uin = request.get_json()['uin']
               access_control_status, access_control_data = update_access_status(uin=uin, allowAccess=True)
               username_status, username_data = lookup_name(uin)
               qir_status, qir_data = update_test_status(uin=uin, test_status="release")
               if not qir_status:
                    abort(500, 'QIR API - ' + qir_data['message'])
               elif not access_control_status:
                    abort(500, 'Access API - ' + access_control_data['message'])
               elif not username_status:
                    abort(500, 'TNC API - ' + username_data['message'])
               else:
                    user_status_obj = {
                         "uin": uin,
                         "given_name": username_data['data']['firstName'],
                         "family_name": username_data['data']['lastName'],
                         "status": access_control_data['data']["allowAccess"]
                    }
                    return {
                         "user": user_status_obj
                    }
          else:
               abort(400, 'UIN is a required field!')
     else:
          abort(403, 'User not Authorized! Please login first.')


# This is the health check for AWS ECS
@app.route('/health')
def health():
    return {'message': 'Healthy'}  # This will return as JSON by default with a 200 status code


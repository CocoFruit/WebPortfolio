from flask import Flask
from flask import *
import random
from flask import Flask, jsonify, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore
import os
import pathlib
import requests
from flask import *
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import time
import collections
import re
import json
from pip._vendor import cachecontrol

app = Flask(__name__)
app.secret_key = 'key'

# Firebase setup
cred = credentials.Certificate(r"C:\Users\parke\Downloads\vote_example\vote_example\creds.json") # /home/ArkerPay/mysite/creds.json
firebase_admin.initialize_app(cred)
db = firestore.client()

# Google OAuth setup
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = "329078169830-850binjjp8lfihtlicvdk1f4rih2fk94.apps.googleusercontent.com"  
flow = Flow.from_client_secrets_file(  
	client_secrets_file=".gitignore/oath.json", # /home/ArkerPay/mysite/.gitignore/oath.json
	scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  
	redirect_uri="http://localhost:80/callback" #FIX THIS WHEN YOU DEPLOY # https://arkerpay.pythonanywhere.com/callback
	)

def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "sub" not in session:  #authorization required
            return redirect("/hshlogin")
        else:
            return function()

    return wrapper

@app.route("/login")  #the page where the user can login
def login():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)

@app.route("/logout")  #the page where the user can login
def logout():
    session.clear()
    return redirect("/")

@app.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    print(id_info)
    # ~ {'iss': 'https://accounts.google.com', 'azp': '55803751818-j3nlbc4p9sau2pnmutubvemldst17slj.apps.googleusercontent.com', 'aud': '55803751818-j3nlbc4p9sau2pnmutubvemldst17slj.apps.googleusercontent.com', 'sub': '104209901845806192943', 'email': 'nicholas.seward@gmail.com', 'email_verified': True, 'at_hash': 'Sb0E7UAmDNVDZFo3Z4wZjg', 'name': 'Nicholas Seward', 'picture': 'https://lh3.googleusercontent.com/a-/AFdZucrtpIlkBU61T_kDCPc9eYFaVcbub79F8P18N9crgQ=s96-c', 'given_name': 'Nicholas', 'family_name': 'Seward', 'locale': 'en', 'iat': 1661021411, 'exp': 1661025011}
    # ~ session["photos"]=[]
    # ~ session["class"]=getClass(id_info.get("email"))
    session.update(id_info)
    
    return redirect("/hsh")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/bio')
def bio():
    return send_from_directory('static', 'bio.html')

@app.route('/favorites')
def favorites():
    return send_from_directory('static', 'favorites.html')

@app.route('/schedule')
def schedule():
    return send_from_directory('static', 'schedule.html')

@app.route('/cringe')
def cringe():
    return send_from_directory('static', 'cringess.html')

@app.route('/zen')
def zen():
    return send_from_directory('static', 'zen.html')

mascots = [ "Buzz the Bee",
            "Tony the Tiger",
            "Count Alfred Chocula",
            "Lucky the Leprechaun",
            "Sonny the Cuckoo Bird",
            "Trix Rabbit"]

@app.route('/quiz')
def quiz():
    if request.method == "GET" and "quiz" in request.args:
        num = int(request.args['quiz'])
        print(num)
        if num == 1:
            session["name"] = request.args["name"]
        elif num == 2:
            session["utensil"]=request.args["utensil"]
        elif num == 3:
            session["superpower"]=request.args["superpower"]
        elif num == 4:
            session["spirit"]=request.args["spirit"]
        elif num == 5:
            session["smell"]=request.args["smell"]
        elif num == 6:
            session["dance"]=request.args["dance"]
        elif num == 7:
            session["transport"]=request.args["transport"]

            # Generate a random seed based on the user's answers
            seed = hash((session["name"], session["utensil"], session["superpower"], session["spirit"], session["smell"], session["dance"], session["transport"]))
            random.seed(seed)

            # Randomly select a mascot for this session
            session["mascot"] = random.choice(mascots)

            session["image"] = f"static/images/{session['mascot'].lower().replace(' ','')}.webp"
            return render_template('finalmsg.html', **session)
        return render_template(f'form{num+1}.html',**request.args)
    return render_template('form1.html')

@app.route('/wouldyourather')
def wouldyourather():
    return render_template('wouldyourather.html')

@app.route('/maya')
def maya():
    return send_from_directory('static','flowers.html')

@app.route('/vote', methods=['GET'])
def vote():
    votes_ref = db.collection('votes')
    question = request.args.get('question')
    option = request.args.get('option')
    
    # Update the vote count for the selected option in Firestore
    vote_doc = votes_ref.document(question)   

    # if the document doesn't exist, create it
    if not vote_doc.get().exists:
        vote_doc.set({option: 0})

    vote_data = vote_doc.get()
    vote_data_dict = vote_data.to_dict()

    if vote_data.exists:
        vote_count = vote_data_dict.get(option, 0) + 1
    else:
        vote_count = 1
    
    vote_data_dict[option] = vote_count
    vote_doc.set(vote_data_dict)
    
    return jsonify(vote_data_dict)

@app.route('/list')
def todolist():
    docs = db.collection('todo_list').stream()
    output = []
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict["_id"] = doc.id
        output.append(doc_dict)

    return jsonify(output)
    
@app.route('/toggle/<doc_id>')
def toggle(doc_id):
    docref = db.collection('todo_list').document(doc_id)
    doc = docref.get()
    if doc.exists:
        is_complete = doc.to_dict().get('is_complete', False)
        docref.update({"is_complete": not is_complete})
    return ""

@app.route('/add', methods=['GET'])
def add_item():
    if "item" in request.args:
        item=request.args["item"]
        db.collection('todo_list').add({
            'item': item,
            'is_complete': False,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    return ""

@app.route('/delete/<doc_id>', methods=['GET'])
def delete_item(doc_id):
    db.collection('todo_list').document(doc_id).delete()
    return ""

@app.route('/todo')
def todo():
    return send_from_directory('static','list.html')

@app.route('/weather')
def weather():
    return send_from_directory('static','weather.html')

@app.route('/hsh')
@login_is_required
def hsh():
    return render_template('hsh.html', **session)

@app.route('/hshlogin')
def hshlogin():
    return send_from_directory('static','hshlogin.html')

@app.route('/hshgetuser', methods=['GET'])
def hshgetuser():
    if db.collection('spaceship').document(session["sub"]).get().exists:
        spaceship = db.collection('spaceship').document(session["sub"]).get().to_dict()
        return jsonify(spaceship)
    else:
        # set default spaceship
        db.collection('spaceship').document(session["sub"]).set({
            'activated': '[0,0,0]'
        })
        return jsonify({'activated': '[0,0,0]'})
    
@app.route('/hshset', methods=['GET'])
def hshset():
    if "activated" in request.args:
        activated = request.args["activated"]
        db.collection('spaceship').document(session["sub"]).set({
            'activated': activated
        })
        return jsonify({'activated': activated})
    return jsonify({'activated': '[0,0,0]'})

@app.route('/hshgetflag', methods=['GET'])
def hshgetflag():
    # if user activated == [1,1,1] return flag
    if db.collection('spaceship').document(session["sub"]).get().exists:
        spaceship = db.collection('spaceship').document(session["sub"]).get().to_dict()
        print(spaceship["activated"])
        if spaceship["activated"] == "[0,0,1]" or spaceship["activated"] == "[0,1,1]" or spaceship["activated"] == "[1,0,1]":
            return jsonify({'flag': 'flag{hsh_1s_c00l}'})
        else:
            return jsonify({'flag': 'not yet'})
    else:
        return jsonify({'flag': 'not yet'})

@app.route('/boggle')
def boggle():
    return render_template('boggle.html', **session)

@app.route('/update-color', methods=['GET','POST'])
def update_color():
    print("here")
    for item in request.args:
        print(request.args[item])
        if item == "color":
            color = request.args[item]
            db.collection('users').document(session["sub"]).set({
                'color': color
            })
            return jsonify({session['sub']: color,"success":True})
    
    return jsonify({session['sub']: ""})
    # # send to database as sub:color:color
    # data = request.get_json()
    # color = data.get('color')
    
    # # Update the color in the database
    # db.collection('users').document(session["sub"]).set({
    #     'color': color
    # })
    
    # return jsonify({session['sub']: color})

@app.route('/get-color', methods=['GET','POST'])
def get_color():
    # send to database as sub:color:color
    # see if the user has a color
    if db.collection('users').document(session["sub"]).get().exists:
        color = db.collection('users').document(session["sub"]).get().to_dict()["color"]
        return jsonify({"color": color,"success":True})
    else:
        return jsonify({"color": 'black'})

if __name__=="__main__":
    app.run(host='0.0.0.0',port=80)
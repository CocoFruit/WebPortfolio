from flask import Flask
from flask import *
import random


app = Flask(__name__)
app.secret_key = 'key'

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

if __name__=="__main__":
    app.run(host='0.0.0.0',port=80)
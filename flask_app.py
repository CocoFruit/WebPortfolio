from flask import Flask
from flask import *

app = Flask(__name__)

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

'''
app.route('/quiz')
def quiz():
    quiz = {"title":"title","1":{"option1":"option1","option2":"option2"}}
    if request.method == "GET" and "quiz" in request.args:
        return render_tempalte(f"form.html",previtem=previtems,question=quiz[request.args["quiz"]])
    return render_template("form.html",question=quiz["1"])
'''

if __name__=="__main__":
    app.run(host='0.0.0.0',port=80)
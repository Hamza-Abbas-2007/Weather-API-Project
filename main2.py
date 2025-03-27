from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from diskcache import Cache

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
cache = Cache('./cache_directory')

class todo (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<task %r>' % self.id
    
API_KEY = 'PM66FQJM5T8WARQP2K4NH8UVM'
url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/cairo?unitGroup=metric&include=days&key={API_KEY}"
response = requests.get(url)
print(response.status_code)
jsonData = response.json()

info = jsonData["days"][0]
temp = info["temp"]

def Get_weather():
    if 'weather' in cache:
        print("already cached")
        return cache['weather']
    if response.status_code == 200:
        cache.set('weather', temp, expire = 3600)
        print ("cached sucessfully")
        return temp

cachedtemp = Get_weather()
    

@app.route('/' ,methods = ['post','get'])
def index():
    
    if request.method == 'POST':
        new_temp = todo(content = str(cachedtemp))
        try:
            db.session.add(new_temp)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding the data to the database'
    
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html' ,tasks = tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_delete = todo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
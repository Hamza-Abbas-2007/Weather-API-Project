from flask import Flask,render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
from diskcache import Cache
import sys
sys.stdout.write("Hello")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
cache = Cache('./cache_directory')

class todo (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    city_name = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<task %r>' % self.id
    
API_KEY = 'PM66FQJM5T8WARQP2K4NH8UVM'

def Get_weather(city):
    cache_key = f'weather_{city}'
    
    if cache_key in cache:
        print("Cache hit: Returning cached temperature")
        return cache[cache_key]

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days&key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        jsonData = response.json()
        temp = jsonData["days"][0]["temp"]
        
        cache.set(cache_key, temp, expire=60)
        print(f"Cached successfully for {city}")
        return temp

@app.route('/' ,methods = ['post','get'])
def index():
    city = request.form.get('city')
    cachedtemp = Get_weather(city) 
    if request.method == 'POST':
    
        new_entry = todo(content=str(cachedtemp), city_name=str(city))
        try:
            if todo.query.count() < 10:
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/')
            else:
                oldest_entry = todo.query.order_by(todo.date_created.asc()).first()
                db.session.delete(oldest_entry)
                db.session.commit()
                
                db.session.add(new_entry)
                db.session.commit()
                return redirect('/')
                
                
        except:
            return 'there was an issue adding the data to the database'
        
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html' ,tasks = tasks,)

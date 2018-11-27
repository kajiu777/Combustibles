from flask import Flask, render_template, abort, request, jsonify
from sklearn.externals import joblib 
import pickle
import pymysql


app = Flask(__name__)

@app.route('/ruta', methods=['post', 'get'])
def Index():
  if request.method == 'POST':
    mes = int(request.form['mes'])
    estado = int(request.form['estado'])
    tipo_combustible = request.form['tipo_combustible']

    if tipo_combustible == 'Diesel':
      modelo = joblib.load("predictdiesel.pkl")
    if tipo_combustible == 'Magna':
      modelo = joblib.load("predictmagna.pkl")
    if tipo_combustible == 'Premium':
      modelo = joblib.load("predictpremium.pkl")
      
    prediction = (modelo.predict([[mes,estado]])).tolist()

    return jsonify({'prediction': prediction})
  if request.method == 'GET':
    return render_template('ruta.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.prediction['numeroserie']
    processed_text = text.upper()
    return processed_text


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "usuario"
        password = "123456"
        db = "combustible"

        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_combustible(self):
        self.cur.execute("SELECT Estado, Dieselcosto, Magnacosto,	Premiumcosto ,Anio, Mes FROM historia")
        result = self.cur.fetchall()

        return result

@app.route('/base')
def combustible():

    def db_query():
        db = Database()
        emps = db.list_combustible()

        return emps

    res = db_query()

    return render_template('tabla.html', result=res, content_type='application/json')

if __name__ == '__main__':
  app.run(port = 8000, debug = True)

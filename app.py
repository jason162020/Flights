
from flask import Flask,render_template,session,request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker





engine=create_engine('postgresql://postgres:monster@localhost/flights')
db=scoped_session(sessionmaker(bind=engine))

app=Flask(__name__)
app.run(debug=True)
@app.route('/')
def home():
	flights=db.execute("SELECT * FROM flights").fetchall()
	return render_template('home.html',flights=flights)

@app.route('/book',methods=['POST'])
def book():
	name=request.form.get('name')
	flight_id=request.form.get('flight_id')
	db.execute("INSERT INTO passengers(name,flight_id)VALUES(:name,:flight_id)",{'name':name,'flight_id':flight_id})
	db.commit()

	return 'Flight booked'
@app.route('/flight_details/<int:flight_id>')
def flight_details(flight_id):
	flight=db.execute("SELECT * FROM flights WHERE id=:flight_id",{'flight_id':flight_id}).fetchone()
	passengers=db.execute("SELECT * FROM passengers WHERE flight_id=:f_id",{'f_id':flight_id}).fetchall()

	return	render_template('flight_details.html',flight=flight,passengers=passengers)


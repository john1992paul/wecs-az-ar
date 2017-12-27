import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask import session as session
import csv
import sqlite3
from gtts import gTTS
from playsound import playsound


app = Flask(__name__)

def dict_gen(curs):
    import itertools
    field_names = [d[0].lower() for d in curs.description]
    while True:
        rows = curs.fetchmany()
        if not rows: 
        	return
        for row in rows:
            yield dict(zip(field_names, row))

@app.route('/')
def index():
	session['row_number'] = 0
	session['counter'] = 0
	id = 0
	poi = "Enter a city to start collecting Data"
	session['completed'] = 0
	session['total'] = 0
	session['state'] = "No man's land"
	session['message'] = ''

	data = {
		'id': id,
		'poi': poi,
		'completed': session['completed'],
		'total': session['total'],
		'state': session['state'],
		'message': session['message']
	}
	return render_template('google.html', data = data)

@app.route('/send_data', methods = ['POST'])
def send_data():
	try:
		start_row_number = int(request.form["start_row_number"])
		state = request.form["state"]
		session['state'] = state
		session['row_number'] = start_row_number
		database = session['state'] + '.db'
		con = sqlite3.connect(database)
		cursor = con.execute("SELECT count(*) as count FROM poi;")
		item = [r for r in dict_gen(cursor)]
		session['total'] = item[0]['count']

		cursor = con.execute("SELECT * FROM poi where row_number=" + str(start_row_number) +";")
		item = [r for r in dict_gen(cursor)]
		item[0]['count'] = session['total']
		item[0]['message'] = 0
		item[0]['completed'] = session['row_number']-1
	except:
		item = [{'message': 1, 'message_text': 'Invalid Starting Row Number Entered'}]
		return jsonify(item)

	try:
		print(item[0]['poi'])
	except:
		item = [{'message': 1, 'message_text': 'Invalid Starting Row Number Entered'}]
		return jsonify(item)

	session['row_number'] = start_row_number
	return jsonify(item)

@app.route('/next_data', methods = ['POST'])
def next_data():

	session['row_number'] +=1
	if session['total'] == 0:
		session['row_number']-=1
		item = [{'message': 1, 'message_text': 'Choose a State'}]
		return jsonify(item)
	if session['row_number'] <= session['total']:
		database = session['state'] + '.db'
		con = sqlite3.connect(database)
		cursor = con.execute("SELECT * FROM poi where row_number=" + str(session['row_number']) +";")
		item = [r for r in dict_gen(cursor)]
		item[0]['completed'] = session['row_number']-1
		item[0]['message'] = 0
		#print(item)
	else:
		session['row_number']-=1
		item = [{'message': 1, 'message_text': 'Hurray!! You finished collecting ' + session['state']}]
		return jsonify(item)

	return jsonify(item)

@app.route('/previous_data', methods = ['POST'])
def previous_data():
	session['row_number'] -=1
	if session['total'] == 0:
		session['row_number']-=1
		item = [{'message': 1, 'message_text': 'Choose a State'}]
		return jsonify(item)
	if session['row_number'] > 0:
		database = session['state'] + '.db'
		con = sqlite3.connect(database)
		cursor = con.execute("SELECT * FROM poi where row_number=" + str(session['row_number']) +";")
		item = [r for r in dict_gen(cursor)]
		item[0]['completed'] = session['row_number']-1
		item[0]['message'] = 0
		#print(item)
	else:
		session['row_number']+=1
		item = [{'message': 1, 'message_text': 'Row number less than 1 doesnot exist' + session['state']}]
		return jsonify(item)

	return jsonify(item)


@app.route('/speak', methods = ['POST'])
def speak():
	speech_text = request.form['speech_text']
	try:
		filename = "/static/"+str(session['counter']) + ".mp3"
		os.remove(filename)
	except:
		pass

	session['counter']+=1
	filename = "./static/"+str(session['counter']) + ".mp3"
	tts = gTTS(text = speech_text, lang='en-uk')
	tts.save(filename)
	
	return filename.split('.')[1]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4450))
    app.debug = True
    app.secret_key = 'Abjojo.555'
    app.run(host='0.0.0.0', port=port)
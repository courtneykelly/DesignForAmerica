from flask import Flask, render_template, request, jsonify, url_for, redirect, make_response, session

from database_functions import *

import requests
import datetime

app = Flask(__name__)
app.secret_key = 'This is a secret'

@app.route('/')
def home():
	try:
		posts = getAllPosts()
		return render_template( 'home.html', posts = posts )
	except KeyError:
		print "Error!"
		return render_template( 'home.html' )

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/createAccount')
def createAccount():
	return render_template('createAccount.html')

if __name__ == "__main__":
	app.run()
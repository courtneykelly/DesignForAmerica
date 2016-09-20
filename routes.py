from flask import Flask, render_template, request, jsonify, url_for, redirect, make_response, session, flash
from functools import wraps
from database_functions import *

import requests
import datetime

app = Flask(__name__)
app.secret_key = "you shall not pass"

# Login Required Function
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session: 
			return test(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def home():
	try:
		posts = getAllPosts()
		return render_template( 'home.html', posts = posts )
	except KeyError:
		print "Error!"
		return render_template( 'home.html' )

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':
		user = findUser(request.form['username'])
		if user:
			if request.form['password'] == user[0][4]:
				session['logged_in'] = True
				session['firstname'] = user[0][0]
				session['lastname'] = user[0][1]
				session['accounttype'] = user[0][2]
				session['username'] = user[0][3]
				session['password'] = user[0][4]
				session['email'] = user[0][5]
				flash('You were just logged in!')
				return redirect(url_for('home'))
			else:
				error = 'Incorrect password! Try again!'
				return render_template('login.html', error=error)
		else:
			error = 'Username does not exist!'
			return render_template('login.html', error=error)
	return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
	error = None
	session.pop('logged_in', None)
	flash('You were just logged out!')
	return redirect(url_for('backToHome', error=error))

@app.route('/createAccount', methods=['GET', 'POST'])
def createAccount():
	error = None
	if request.method == 'POST':
		if request.form['accounttype'] == 'Administrator' and request.form['accesscode'] == 'Harambe2016':
			flash('Successful Administrator Access!')
		if request.form['accounttype'] == 'Administrator' and request.form['accesscode'] != 'Harambe2016':
			error = 'Invalid Administrator Access Code'
			return render_template('createAccount.html', error=error)			
		if request.form['password'] != request.form['password_confirm']:
			error = 'Passwords do not match!'
			return render_template('createAccount.html', error=error)

		firstname = str(request.form['firstname'])
		session['firstname'] = request.form['firstname']
		lastname = str(request.form['lastname'])
		session['lastname'] = request.form['lastname'] 
		accounttype = str(request.form['accounttype'])
		session['accounttype'] = request.form['accounttype']
		username = str(request.form['username'])
		session['username'] = request.form['username']
		password = str(request.form['password'])
		session['password'] = request.form['password']
		email = str(request.form['email'])
		session['email'] = request.form['email']


		addUser(firstname, lastname, accounttype, username, password, email)
		flash('Account Creation Successful!')
		return render_template('backToHome.html', error=error)

	return render_template('createAccount.html', error=error)

@app.route('/newPost', methods=['GET', 'POST'])
def newPost():
	if request.method == 'POST':
		postTitle = str(request.form['postTitle'])
		postCategory = str(request.form['postCategory'])
		postBody = str(request.form['postBody'])

		if session.get('username'):
			username = session['username']
		else:
			username = "Unknown user"

		date = datetime.datetime.now()
		date_string = str(date.month) + "/" + str(date.day) + "/" + str(date.year)

		addPost(username, postTitle, postCategory, postBody, date_string)
		return render_template('backToHome.html')

	return render_template('newPost.html')

@app.route('/backToHome')
def backToHome():
	error = None
	return render_template('backToHome.html', error=error)

@app.route('/UCC Experience')
def uccExperience():
	try:
		posts = getCategoryPosts('UCC Experience')
		return render_template('ucc.html', posts = posts)
	except KeyError:
		return render_template('ucc.html')

@app.route('/Concern for Others')
def concernForOthers():
	try:
		posts = getCategoryPosts('Concern for Others')
		return render_template('concernForOthers.html', posts = posts)
	except KeyError:
		return render_template('concernForOthers.html')

@app.route('/Relationships')
def relationships():
	try:
		posts = getCategoryPosts('Relationships')
		return render_template('relationships.html', posts = posts)
	except KeyError:
		return render_template('relationships.html')

@app.route('/General')
def general():
	try:
		posts = getCategoryPosts('General')
		return render_template('general.html', posts = posts)
	except KeyError:
		return render_template('general.html')

@app.route('/Other')
def other():
	try:
		posts = getCategoryPosts('Other')
		return render_template('other.html', posts = posts)
	except KeyError:
		return render_template('other.html')

@app.route('/fullPost/<postID>', methods=['GET', 'POST'])
def expandPost(postID):
	if request.method == 'POST':
		newResponse = str(request.form['newResponse'])
		addResponse(postID, newResponse)
		comments = getComments(getPost(postID))
		
		post = getPost(postID)
		return redirect(url_for('backToHome'))

	try:
		post = getPost(postID)
		comments = getComments(post)
		return render_template('fullPost.html', post = post, comments = comments)
	except KeyError:
		return render_template('fullPost.html')

@app.route('/deleteComment/<postID>&<comment>', methods=['POST'])
def deleteComment(postID, comment):
	if request.method == 'POST':
		deleteComment(postID, comment)
		flash('Your comment was successfully deleted!')
		return redirect(url_for('backToHome'))

	return redirect(url_for('/fullPost/<postID>'))

@app.route('/delete/<postID>', methods=['POST'])
def delete(postID):
	try:
		deletePost(postID)
		flash('Your post was successfully deleted!')
		return redirect(url_for('backToHome'))
	except KeyError:
		return render_template('yourPosts.html')

@app.route('/yourPosts')
def yourPosts():
	try:
		posts = getUserPosts(session['username'])
		return render_template('yourPosts.html', posts = posts)
	except KeyError:
		return render_template('yourPosts.html')

@app.route('/about')
def about():
	try:
		return render_template('about.html')
	except KeyError:
		return render_template('about.html')

@app.route('/additionalResources')
def additionalResources():
	try:
		return render_template('additionalResources.html')
	except KeyError:
		return render_template('additionalResources.html')



if __name__ == "__main__":
	app.run()
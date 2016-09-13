import sqlite3 as lite

database = 'posts.sqlite'
userbase = 'users.sqlite'

def addPost(user, postTitle, postCategory, postBody, submit_date):
	data = [user, postTitle, postCategory, postBody, submit_date]
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		c.executemany('INSERT INTO posts VALUES(?,?,?,?,?)',(data,))

def getAllPosts():
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		sql = "SELECT * FROM posts"
		c.execute(sql)
		posts = c.fetchall()
	return posts

def getCategoryPosts(category):
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		query = 'SELECT * FROM posts WHERE postCategory = "' + category + '"'
		c.execute(query)
		posts = c.fetchall()
		return posts

def addUser(firstName, lastName, accountType, username, password, email):
	newUser = [firstName, lastName, accountType, username, password, email]
	conn = lite.connect(userbase)
	with conn:
		c = conn.cursor()
		c.executemany('INSERT INTO users VALUES(?,?,?,?,?,?)',(newUser,))

def findUser(username_query):
	conn = lite.connect(userbase)
	with conn:
		c = conn.cursor()
		query = 'SELECT * FROM users WHERE username = "' + username_query + '"'
		c.execute(query)
		user = c.fetchall()
		return user






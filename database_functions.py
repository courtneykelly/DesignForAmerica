import sqlite3 as lite

database = 'posts.sqlite'
userbase = 'users.sqlite'

def addPost(user, postTitle, postCategory, postBody, submit_date):
	data = [None, user, postTitle, postCategory, postBody, submit_date, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,]
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		c.executemany('INSERT INTO posts VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(data,))

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

def getUserPosts(username):
	conn = lite.connect(database)
	with conn: 
		c = conn.cursor()
		query = 'SELECT * FROM posts WHERE user = "' + username + '"'
		c.execute(query)
		posts = c.fetchall()
		return posts

def getPost(postID):
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		query = 'SELECT * FROM posts WHERE PostID = "' + postID + '"'
		c.execute(query)
		post = c.fetchall()
		return post

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

def deletePost(postID):
	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		query = 'DELETE FROM posts WHERE PostID = "' + postID + '"'
		c.execute(query)

def getCommentNum(post):
	for num in range(6,44):
		if post[0][num] == None:
			return num

def getComments(post):
	comments = []
	for num in range(6,44):
		if post[0][num] != None:
			comments.append(post[0][num])
	return comments

def getCommentLocation(postID, comment):
	post = getPost(postID)
	for num in range(6,44):
		if post[0][num] == comment:
			return num

def addResponse(postID, newResponse):
	post = getPost(postID)
	commentID = getCommentNum(post)
	label = "c" + str(commentID-4)

	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		c.execute('UPDATE posts SET "' + label + '" = ? WHERE PostID = "' + postID + '"',(newResponse,))

def deleteResponse(postID, comment):
	postID = str(postID)
	commentLocation = getCommentLocation(postID, comment)
	label = "c" + str(commentLocation-4)

	conn = lite.connect(database)
	with conn:
		c = conn.cursor()
		c.execute('UPDATE posts SET "' + label + '" = NULL WHERE PostID = "' + postID + '"')

def findPostID(comment):
	posts = getAllPosts()

	for post in posts:
		for element in post:
			if element == comment:
				return post[0]







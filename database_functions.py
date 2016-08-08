import sqlite3 as lite

database = 'posts.sqlite'

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
		query = 'SELECT * FROM posts WHERE category = "' + category + '"'
		c.execute(query)
		posts = c.fetchall()
		return posts
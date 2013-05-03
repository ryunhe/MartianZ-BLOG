import tornado.ioloop
import tornado.web
import markdown
import codecs
import os

settings = {
	"title": "Mocha",
	"url": """http://mocha.cc""",
	"posts_dir": "%s%sposts" % (os.getcwd(), os.sep),
	"static_path": os.path.join(os.path.dirname(__file__), "static"), # settings for static_url
}


def MarkdownParser(path):
	file = codecs.open(path, mode='r', encoding='utf8')
	result = {}
	lines = []
	try:
		lines = file.readlines()
	except:
		pass
	file.close()

	for line in lines[1:]:
		if line.find('title: ') == 0:
			result['title'] = line.replace('title: ', '')[0:-1]
		if line.find('date: ') == 0:
			result['date'] = line.replace('date: ', '')[0:-1]
		if line.find('---') == 0:
			break

	if result['title']:
		content = u''
		for line in lines[4:]:
			content += line
		result['content'] = markdown.markdown(content)
		result['name'] = path.split(os.sep)[-1].split('.')[0]

	return result


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		page = int(self.get_argument('p', '0'))
		posts_dir = settings["posts_dir"]
		files = os.listdir(posts_dir)

		posts = []

		for f in files:
			posts.append(posts_dir + os.sep + f)

		posts.sort(reverse=True)

		articles = []
		for path in posts[page:page + 3]:
			article = MarkdownParser(path)
			if article:
				articles.append(article)

		self.render("views/index.html", title=settings['title'], url=settings["url"], articles=articles,
					prev=page > 2, next=page + 4 <= len(articles), prevnum=page - 3, nextnum=page + 3)


class ArticleHandler(tornado.web.RequestHandler):
	def get(self, name):
		path = settings["posts_dir"] + os.sep + name + '.md'
		article = MarkdownParser(path)
		self.render("views/article.html", title=settings['title'], url=settings["url"], article=article)


class NotFoundHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_status(404)
		self.render("views/notfound.html", title=settings['title'], url=settings["url"])


app = tornado.web.Application(
	[
		(r"/", MainHandler),
		(r"/articles/(.*)", ArticleHandler),
		(r"/.*", NotFoundHandler),
	], **settings)

if __name__ == "__main__":
	app.listen(8888)
	tornado.ioloop.IOLoop.instance().start()

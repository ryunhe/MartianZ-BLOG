import tornado.ioloop
import tornado.autoreload
import tornado.web
import markdown
import codecs
import os
import re

confs = {
	'posts_dir': '%s%sposts' % (os.getcwd(), os.sep),
	'listen_port': 7777,
	'autoreload': False,
}

settings = {
	'static_path': os.path.join(os.path.dirname(__file__), 'static'),
	'xsrf_cookies': True,
}


def MarkdownParser(path):
	result = {}
	lines = []
	file = codecs.open(path, mode='r', encoding='utf8')
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
		posts = []
		for file in os.listdir(confs["posts_dir"]):
			if re.search('\.md$', file):
				posts.append(confs["posts_dir"] + os.sep + file)

		posts.sort(reverse=True)

		articles = []
		for path in posts[page:page + 3]:
			article = MarkdownParser(path)
			if article:
				articles.append(article)

		self.render("views/index.html", articles=articles,
					prev=page > 2, next=page + 4 <= len(articles),
					prevnum=page - 3, nextnum=page + 3)


class ArticleHandler(tornado.web.RequestHandler):
	def get(self, name):
		path = confs["posts_dir"] + os.sep + name + '.md'
		article = MarkdownParser(path)
		self.render("views/article.html", article=article)


class NotFoundHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_status(404)
		self.render("views/notfound.html")


app = tornado.web.Application(
	[
		(r"/", MainHandler),
		(r"/articles/(.*)", ArticleHandler),
		(r"/.*", NotFoundHandler),
	], **settings)

if __name__ == "__main__":
	app.listen(confs['listen_port'])
	loop = tornado.ioloop.IOLoop.instance()
	if confs['autoreload']:
		tornado.autoreload.start(loop)
	loop.start()

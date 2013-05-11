import tornado.ioloop
import tornado.autoreload
import tornado.web
import markdown
import codecs
import sys
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
PORT = 7777
DEBUG = True

settings = {
	'static_path': os.path.join(BASE, 'static'),
	'xsrf_cookies': True,
}


def MarkdownParser(path):
	result = {'name': path.split(os.sep)[-1].split('.')[0]}

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

	content = u''
	for line in lines[4:]:
		content += line
	result['content'] = markdown.markdown(content)

	return result


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		page = int(self.get_argument('p', '0'))
		posts = []
		path = os.path.join(BASE, 'posts', '')

		for file in os.listdir(path):
			if re.search('\.md$', file):
				posts.append(path + file)

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
		article = MarkdownParser(os.path.join(BASE, 'posts', name + '.md'))
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
	app.listen(len(sys.argv) > 1 and int(sys.argv[1]) or PORT)
	loop = tornado.ioloop.IOLoop.instance()
	if DEBUG:
		tornado.autoreload.start(loop)
	loop.start()

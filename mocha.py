import tornado.ioloop
import tornado.autoreload
import tornado.web
import markdown
import codecs
import os
import re


from tornado.options import define, options, parse_command_line

define("port", default=8888, help="Run on the given port", type=int)
define("home", default=os.path.dirname(os.path.abspath(__file__)), help="App home path.")

settings = {
	'static_path': os.path.join(options.home, 'static'),
	'xsrf_cookies': True,
	'debug': True,
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
		path = os.path.join(options.home, 'posts', '')
		current = page * 3

		for file in os.listdir(path):
			if re.search('\.md$', file):
				posts.append(path + file)

		posts.sort(reverse=True)

		articles = []
		for path in posts[current:current + 3]:
			article = MarkdownParser(path)
			if article:
				articles.append(article)

		self.render("views/index.html", articles=articles,
					prev=page > 0, next=current + 4 <= len(posts),
					prevnum=page - 1, nextnum=page + 1)


class ArticleHandler(tornado.web.RequestHandler):
	def get(self, name):
		article = MarkdownParser(os.path.join(options.home, 'posts', name + '.md'))
		self.render("views/article.html", article=article)


class NotFoundHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_status(404)
		self.render("views/notfound.html")

if __name__ == "__main__":
	parse_command_line()
	app = tornado.web.Application(
		[
			(r"/", MainHandler),
			(r"/articles/(.*)", ArticleHandler),
			(r"/.*", NotFoundHandler),
		], **settings)
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

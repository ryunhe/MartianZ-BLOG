import tornado.ioloop
import tornado.autoreload
import tornado.web
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


def PhotoMaker(filename):
	return {
		'path': 'photos/' + filename,
		'date': filename[0:-4]
	}


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		page = int(self.get_argument('p', '0'))
		path = os.path.join(options.home, 'photos', '')
		current = page * 3

		photos = []
		for file in os.listdir(path):
			if re.search('\.jpg$', file):
				photos.append(PhotoMaker(file))

		photos.sort(reverse=True)

		self.render("views/index.html", photos=photos[current:current + 3],
					prev=page > 0, next=current + 4 <= len(photos),
					prevnum=page - 1, nextnum=page + 1)


class NotFoundHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_status(404)
		self.render("views/notfound.html")


if __name__ == "__main__":
	parse_command_line()
	app = tornado.web.Application(
		[
			(r"/", MainHandler),
			(r"/photos/(.*\.jpg)$", tornado.web.StaticFileHandler, dict(path=os.path.join(options.home, 'photos'))),
			(r"/.*", NotFoundHandler)
		], **settings)
	app.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

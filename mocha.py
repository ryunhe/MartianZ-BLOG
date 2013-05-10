import tornado.ioloop
import tornado.autoreload
import tornado.web
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


def PhotoMaker(filename):
	return {
		'path': 'photos/' + filename,
		'date': filename[0:-4]
		}

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		page = int(self.get_argument('p', '0'))
		path = os.path.join(BASE, 'photos', '')

		photos = []
		for file in os.listdir(path):
			if re.search('\.jpg$', file):
				photos.append(PhotoMaker(file))

		photos.sort(reverse=True)

		self.render("views/index.html", photos=photos,
					prev=page > 2, next=page + 4 <= len(photos),
					prevnum=page - 3, nextnum=page + 3)


class NotFoundHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_status(404)
		self.render("views/notfound.html")


app = tornado.web.Application(
	[
		(r"/", MainHandler),
		(r"/photos/(.*\.jpg)$", tornado.web.StaticFileHandler, dict(path='photos')),
		(r"/.*", NotFoundHandler)
	], **settings)

if __name__ == "__main__":
	app.listen(len(sys.argv) > 1 and int(sys.argv[1]) or PORT)
	loop = tornado.ioloop.IOLoop.instance()
	if DEBUG:
		tornado.autoreload.start(loop)
	loop.start()

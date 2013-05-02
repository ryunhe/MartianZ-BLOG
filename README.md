### Dependencies:

1. 
```
	python 2.6 +
	
	easy_install tornado
	easy_install markdown
```

### Usage:

1. 把 .md 文件放在 posts 目标下，并确保每个文件开头有如下标志区域。
```
	---
	title: "对于苹果来说，被大口吃掉才是最重要的。"
	date: 2013-05-02 22:50
	---
```

1. 运行 python app.py 即可，默认监听在 8888 端口上。
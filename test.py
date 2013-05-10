import os



# print __file__

# print  + os.path.dirname(__file__) + os.sep + 'posts'

# print os.path.dirname(__file__) + os.sep + 'posts'

print os.path.abspath(__file__)

print __file__[0] != '/' and os.getcwd() or os.path.dirname(__file__)

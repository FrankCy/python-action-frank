import urllib.request

response = urllib.request.urlopen('http://img16.3lian.com/gif2016/w1/3/d/61.jpg')
image = response.read()

with open('61.jpg','wb') as f:
    f.write(image)
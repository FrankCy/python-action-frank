import urllib.request

# 访问网站
response = urllib.request.urlopen('https://github.com')
# 读取html
html = response.read()
# 输出结果
print(html.decode('utf-8'))
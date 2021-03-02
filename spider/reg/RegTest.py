# 测试正则表达式

import re

line = "bobby123"

# ^ 以什么开头，这是以b开头
# . 任意字符
# * 代表可重复(^b.)
# $ 以什么结尾的，这里是以3结尾的
# |^b|.|*|3$
regex_str = "^b.*3$"

if(re.match(regex_str, line)):
    print("yes")


# 匹配字符串第一个b到第二个b之间的字符串
line2 = "boooooooobbody123"
# ? 代表执行非贪婪模式，不使用?字符串匹配从右至左，使用后从左至右
regex_str2 = ".*?(b.*?b).*"
match_obj = re.match(regex_str2, line2)
if(match_obj):
    print (match_obj.group(1))
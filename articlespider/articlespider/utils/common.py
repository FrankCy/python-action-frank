import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)

    # 生成md5
    return m.hexdigest()

# main方法
if __name__ == "__main__":
    print(get_md5("https://cnblogs.com"))
import string
import urllib.request
import urllib.parse

def choose_engine():
    choose_engine_url = ""
    print("1、百度")
    print("2、谷歌")
    engine = int(input("请选择搜索引擎："))
    if engine == 1:
        choose_engine_url = 'http://www.baidu.com/s?wd='
    elif engine == 2:
        choose_engine_url = 'https://www.google.com/search?q='
    print(choose_engine_url)

    return choose_engine_url


def get_method_params():
    url = choose_engine()
    key_word = input("请输入搜索内容：")
    return url + key_word, key_word

def save_page():
    url, key_word = get_method_params()
    url = urllib.parse.quote(url,safe=string.printable)
    key_word += ".html"
    data = urllib.request.urlopen(url).read().decode("utf-8")
    with open(key_word, "w", encoding="utf-8") as f:
        f.write(data)


if __name__ == '__main__':
    save_page()
    # choose_engine()

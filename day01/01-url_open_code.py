import urllib.request


def load_data():
    url = "http://www.baidu.com"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    print(url)
    with open("baidu.html", "w", encoding="utf-8") as f:
        f.write(data)

if __name__ == '__main__':
    load_data()

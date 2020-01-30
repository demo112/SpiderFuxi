import csv
import random
import time

import parsel
import requests

from proxy_builing import init


class GetIpPort:
    def __init__(self):
        self.proxy = random.random(self.proxy_info_checked)
        self.page_range = 1
        self.headers = {}
        self.proxy_info = []
        self.proxy_info_checked = []
        self.url_list = []
        self.PATH = "/Users/cooper/PycharmProjects/SpiderFuxi/proxy_builing/page_save/"
        self.BASE_URL = "https://www.kuaidaili.com/free/inha/"

    def first_try(self):

        pass


    def make_url(self):
        """根据需要构造url，明确访问多少页"""
        for p in range(self.page_range):
            page_url = self.BASE_URL + str(p + 1) + "/"
            self.url_list.insert(p, page_url)
        # print(self.url_list)

    def make_proxy(self):
        """构造代理信息，防止被网站反爬"""
        random_headers = random.sample(init.UserAgent, 1)[0]
        # print(random_headers)
        self.headers = {"User-Agent": random_headers}
        pass

    def get_page(self):
        """获取真是线上网页"""
        self.make_url()
        for url in self.url_list:
            time.sleep(5)
            self.make_proxy()
            print("正在爬取第%s页" % url[-2:-1])
            # todo 需要继续完善，完善之前，访问本地页面测试
            response = requests.get(url, headers=self.headers, proxies=self.)
            page_data = response.text
            # print(page_data)
            self.page_save(url[-2:-1], page_data)

    def page_save(self, name, save_page):
        """保存网页至本地方便后续使用"""
        name = str(name)
        with open(self.PATH + name + ".html", "w", encoding="utf-8") as linshi:
            linshi.write(save_page)
        pass

    def read_page(self, file_name):
        """读取本地网页"""
        with open(self.PATH + file_name, "r", encoding="utf-8") as r:
            read_page = r.read()
        return read_page
        pass

    def parse_page(self, pars_page):
        """此处是网页解析核心，如网页有变化，重点关注此处"""

        def get_list(page_data):
            """解析表格"""
            html_data = parsel.Selector(page_data)
            parse_list = html_data.xpath("//table/tbody/tr")
            return parse_list

        def get_line(parsed_list):
            """拆分行"""
            lines_list = []
            for line in parsed_list:
                lines_list.append(line)
            return lines_list

        def change_line(line):
            info_dic = {}
            info_dic["ip"] = line.xpath('./td[1]/text()').extract_first()
            info_dic["port"] = line.xpath('./td[2]/text()').extract_first()
            info_dic["proxy_kind"] = line.xpath('./td[3]/text()').extract_first()
            info_dic["http_type"] = line.xpath('./td[4]/text()').extract_first()
            info_dic["location"] = line.xpath('./td[5]/text()').extract_first()
            info_dic["ping"] = line.xpath('./td[6]/text()').extract_first()
            info_dic["check_time"] = line.xpath('./td[7]/text()').extract_first()
            return info_dic

        parsed_list = get_list(pars_page)
        lines_list = get_line(parsed_list)
        for line in lines_list:
            self.proxy_info.append(change_line(line))

    def building_pars_line(self):
        """发起网页解析任务"""
        for p in range(self.page_range):
            file_name = str(p + 1) + ".html"
            page = self.read_page(file_name)
            self.parse_page(page)
        print(self.proxy_info)

    def save_as_csv(self):
        with open("proxy_list_checked.csv", 'w', newline='') as a:
            writer = csv.writer(a)
            writer.writerow(self.proxy_info_checked[0].keys())  # 以字典的键作为表头
            for r in self.proxy_info_checked:
                writer.writerow(r.values())  # 以字典的值作为内容

    def check_ip(self):
        for proxy in self.proxy_info:
            self.make_proxy()
            UserAgent = self.headers
            ip_port = {"http": proxy["ip"] + ":" + proxy["port"]}
            try:
                response_1 = requests.get("https://www.baidu.com", headers=UserAgent, proxies=ip_port, timeout=0.1)
                response_2 = requests.get("https://www.taobao.com", headers=UserAgent, proxies=ip_port, timeout=0.1)
                response_3 = requests.get("https://www.qq.com", headers=UserAgent, proxies=ip_port, timeout=0.1)
                if response_1.status_code == response_2.status_code == response_3.status_code == 200:
                    self.proxy_info_checked.append(proxy)
                    pass
            except Exception as e:
                print(e)

    def choose(self):
        print("1、在线爬取")
        print("2、本地爬取")
        way = input("请选择获取数据的方式：")
        if way == 1:
            self.get_page()
        else:
            pass

    def main(self):
        self.choose()
        self.building_pars_line()
        self.check_ip()
        self.save_as_csv()
        print(len(self.proxy_info_checked))


if __name__ == '__main__':
    get_ip_port = GetIpPort()
    get_ip_port.main()

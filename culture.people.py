import requests
from lxml import etree as etree
import re

hostname = 'http://culture.people.com.cn'
d = 'culture.people.com.cn'
HEADERS = {
    'user-agent':
    r'Mozilla/4.0 (Windows NT 36.0; Win64;x128) AppleWebKit/555.66 (KHTML, like Gecko) Chrome/67.0.1 Safari/555.66'}

def get_pages(url, s=None, encoding='gb2312', headers=HEADERS):
    if s == None:
        s = requests.session()
    s.headers.update(headers)
    try:
        res = s.get(url)
        res.raise_for_status()
        res.encoding = 'gb2312'
        return res.text
    except requests.ConnectTimeout:
        print("requests.ConnectTimeout!")
        return None
    except Exception as e:
        print(e)
        return None


def get_domain(t):
    domain = re.search(r"([a-z]+\.)+[a-z]+", t)
    if domain:
        ret = domain[0]
        # print(ret )
        return ret
    return domain


def spider():
    s = requests.session()
    index = get_pages(hostname, s)
    links = []
    a_list = etree.HTML(index).xpath(
        "//div[ not( contains(@id,'nav')) and not( contains(@class,'nav'))]//a")
    for a in a_list:

        title = a.text
        url = a.xpath('@href[1]')
        if title and url:
            domain = get_domain(url[0])

            if domain == d:
                print(title, url[0])
                links .append([title, url[0]])
            if domain == None:
                print(title, hostname + url[0])
                links.append([title, hostname +  url[0]])
    return  links

if __name__ == '__main__':
    l = spider()
    with open('links_culture_people.txt','w',encoding='gb2312') as f:
        f.writelines(['{}\t{}\n'.format(a[0],a[1]) for a in l ])
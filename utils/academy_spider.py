import json
import time
from random import randint
import lxml
from bs4 import BeautifulSoup
import requests
import re


def write_data(data, index):
    old_data = []
    print('数据本地化...')
    with open('./kugoudata/%s.json'%index, 'w', encoding='utf-8') as file:
        new_data = json.dumps(data, ensure_ascii=False)
        file.write(new_data)
    print('本地化完成!')


def get_page(url):
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]
    while True:
        time.sleep(3)
        headers = {
            "User-Agent": USER_AGENTS[randint(0, len(USER_AGENTS)-1)]
        }
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.content.decode(encoding='utf-8')
        except Exception:
            print('疑似ip限制。。。')
            print(headers)


def get_page_index(index, page='1'):
    if index == '#':
        index = 'null'
    url = 'https://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-20.dhtml'
    html = get_page(url)
    return html


def parse_soup_singer(html, index='a', page='1'):
    dict_index = '%s_%s_singers' % (index, page)
    if page == '1':
        page_data = {'page_list': [], dict_index: {}}
    else:
        page_data = {dict_index: {}}
    soup = BeautifulSoup(html, 'lxml')
    singer_list = soup.find_all('a', href=re.compile('http://www.kugou.com/yy/singer/home/'))
    for singer in singer_list:
        page_data[dict_index][singer.string] = [singer['href']]
    page_list = soup.find_all('a', id=re.compile('page_'))
    if page_data[dict_index].get(None):
        del page_data[dict_index][None]
    if page == '1':
        for page in page_list[2:-2]:
            page_data['page_list'].append(page.string)
    return page_data


def parse_soup_song(singer_song_html):
    soup = BeautifulSoup(singer_song_html, 'html.parser')
    song_list = []
    i_list = soup.select('#song_container > li > a > input')
    for item in i_list:
        song_list.append(item['value'].split('|')[0])
    return song_list


def fetch_song_info(index_data):
    for page_data in index_data:
        for dict_index in page_data.keys():
            if dict_index != 'page_list':
                for singer_name in page_data[dict_index].keys():
                    singer_song_html = get_page(page_data[dict_index][singer_name][0])
                    if singer_song_html != None:
                        song_list = parse_soup_song(singer_song_html)
                    else:
                        song_list = []
                    if len(song_list) != 0:
                        page_data[dict_index][singer_name].append(song_list)
                    else:
                        print(singer_name)
                        print(singer_song_html)
                    print(song_list)


def main():
    string = 'yz#'
    for index in string:
        index_data = []
        index_html = get_page_index(index)
        print('+++++++++++++++++++++++++%s开始+++++++++++++++++++++++++++'%index)
        print(index_html)

if __name__ == '__main__':
    main()

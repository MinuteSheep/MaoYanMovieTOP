import requests
from bs4 import BeautifulSoup
import re


url = 'http://maoyan.com/board/4'
headers ={
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}

def get_html(url):
    response = requests.get(url,headers = headers)
    if response.status_code == 200:
        return response.text
    else:
        return None

def page_parse(html):
    soup = BeautifulSoup(html,'lxml')
    alltop = soup.find_all('i',class_='board-index')
    tops = [t.get_text() for t in alltop]
    alltile = soup.find_all('p',class_='name')
    tiles = [t.find('a')['title'] for t in alltile]
    allactor = soup.find_all('p',class_='star')
    actors = [p.get_text().strip()[3:] for p in allactor]
    alltime = soup.find_all('p',class_='releasetime')
    times = [t.get_text().strip()[5:] for t in alltime]
    pattern = re.compile('<i class="integer">(.*?)</i><i class="fraction">(.*?)</i>',re.S)
    ans = re.findall(pattern,html)
    scores = [a[0]+a[1] for a in ans]
    f = open('猫眼TOP100.txt', 'a', encoding='utf-8')
    for top,title,actor,time,score in zip(tops,tiles,actors,times,scores):
        top = 'Top:' + top + '\n'
        title = 'Title:'+title+'\n'
        actor = 'Actor:'+actor+'\n'
        time = 'Time:'+ time + '\n'
        score = 'Score' + score +'\n'
        data = top + title + actor +time + score
        f.write(data + '======================================' + '\n')
    f.close()






def main():

    for i in range(10):
        html = get_html('http://maoyan.com/board/4?offset=' + str(i*10))
        page_parse(html)
    print('Done!!!')


if __name__ == '__main__':
    main()
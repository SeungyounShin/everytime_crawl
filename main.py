import requests,re
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ElementTree

class Everytime:
    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

    def get_timetable(self, year, semester):
        result_xml = ""
        payload = {'userid': self.userid, 'password': self.password}
        login_url = 'https://everytime.kr/user/login'

        with requests.Session() as session:
            login_ = session.post(login_url, data=payload)
            #print('login response : ',index_page_res)
            #print(soup)
            #token = soup.find(id="userToken")["value"]

            timetable_result = session.post("http://timetable.everytime.kr/ajax/timetable/wizard/getTableList", data={
                "semester": semester,
                "year": year,
                #"token": token
            })


            tree = ElementTree.fromstring(timetable_result.text)
            for target in tree.findall('table[@is_primary="1"]'):
                id = target.get('id')
                table_xml = session.post("http://timetable.everytime.kr/ajax/timetable/wizard/getOneTable", data={
                    "id": id,
                    #"token": token
                })
                result_xml = table_xml

        return result_xml.text
        #return soup

    def crawl_hotarticle(self,how_many_pages):
        hot_base_url = 'https://everytime.kr/hotarticle/p/'
        login_url = 'https://everytime.kr/user/login'
        payload = {'userid': self.userid, 'password': self.password}
        raw = ''
        with requests.Session() as session:
            login_ = session.post(login_url, data=payload)

            for i in range(how_many_pages):
                articles = session.post("http://everytime.kr/find/board/article/list", data={
                    'id': 'hotarticle',
                    'limit_num' : 20,
                    'start_num' : i*20,
                    #"token": token
                    })
                raw += articles.text

            return raw


username = '-'
password = '-'
e = Everytime(username, password)

#timetable
year = 2018
semester = 2
timetable = e.get_timetable(year, semester)

f = open('./data/'+username+'_'+str(year)+'_'+str(semester),'w')
f.write(str(timetable))
f.close()
print(username, 'file saved\n')

pat = re.compile(r'(([01]\d|2[0-3]):([0-5]\d)|24:00)-(([01]\d|2[0-3]):([0-5]\d)|24:00)')

#hotarticle crawl
hotarticles = e.crawl_hotarticle(50)
f = open('./articles/hotarticles','w')
f.write(str(hotarticles))
f.close()
print('hot articles are saved\n')

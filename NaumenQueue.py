from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
from urllib3.util import Retry

from bs4 import BeautifulSoup
import requests
import re
import tkinter as tk
login = 'login'
password = 'password'

def requests_retry_session(
    retries=30,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    values = {'login': login,
              'password': password
              }
    with requests.Session() as sesh:
        #response = requests_retry_session(session=s).get('https://www.peterbe.com')
        r = requests_retry_session(session=sesh).get(url, headers=headers)
        r = requests_retry_session(session=sesh).post(url, data=values)
        r = requests_retry_session(session=sesh).get("http://172.11.1.11:8080/published?uuid=fctsListView")
        return r.text

def bs4Soup(html):
    soup = BeautifulSoup(html, 'lxml')
    html_list = soup.find_all('span')
    list1 = []
    dicct = {}
    for i in html_list:
        list = re.findall(r'[А-яA-z]+|[0-9]+', i.text)
        txt = " ".join(list)
        if "СПБ" in txt or txt.isdigit() == True:
            list1.append(txt)

    print(len(list1))
    print(list1)

    for y in range(1,60,3):
        try:
            dicct[list1[y]] = list1[y+1]
        except:
            pass

    string = ""
    global amount
    amount = 0
    for key in dicct:
        dicct[key] = int(dicct[key])
        amount += dicct[key]
        print(key + "  -  " + str(dicct[key]))
        print(key.replace("СПБ", "").replace('МЕД', '').replace("Очередь", '').replace('проекта', '')\
                  .replace('1', '').replace('2', '').replace('3', '').strip() + "  -  " + str(dicct[key]))
        string += key.replace("СПБ", "").replace('МЕД', '').replace("медицинская", "мед.").replace("Консультация", "Конс.").replace("приложению", "прил.").replace("Очередь", '').replace('проекта', '')\
                  .replace('1', '').replace("Общая очередь Xup", "Xoup").replace('2', '').replace('3', '').strip() + "  -  " + str(dicct[key]) + "\n"
        #string += key.replace("Общая очередь Xoup", 'Xoup')
    return string + "\n" + "Всего   -   " + str(amount)

def main():
    url = "http://172.11.1.11:8080/"
    bs4Soup(get_html(url))

def Draw():
    global text
    frame=tk.Frame(window,width=1000,height=1000,bd=100,bg ='#a9aeb0')
    frame.place(relx=.5, rely=.5, anchor="center")
    text=tk.Label(window)
    text.pack(fill = 'both', expand=True)

def Refresher():
    url = "http://172.11.1.11:8080/"
    global text
    try:
        if int(bs4Soup(get_html(url))[-4:]) > 50:
            bg = '#eb6788'
        elif int(bs4Soup(get_html(url))[-4:]) > 70:
            bg = '#e3869d'
        else:
            #bg = '#333333'
            bg = '#a9aeb0'
    except:
        #bg = '#333333'
        bg = '#a9aeb0'
    text.configure(text=bs4Soup(get_html(url)), font=("Verdana", 55, "bold"), fg="black", bg=bg)
    #fg='#CCCCCC'
    window.after(5000, Refresher) # every second...

window = tk.Tk()
window.title("Гарант")
window.geometry("518x170")
window.configure(background='#333333')
#window.configure(background='#a9aeb0')
window.wm_attributes('-fullscreen', True) # Windows
#window.attributes('-zoomed', True)

Draw()
Refresher()
window.mainloop()

from bs4 import BeautifulSoup
import requests
import re
import tkinter as tk
login = ''
password = ''


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }

    values = {'login': login,
              'password': password
              }
    with requests.Session() as sesh:
        r = sesh.get(url, headers=headers) #Login URL
        r = sesh.post(url, data=values)
        r = sesh.get("http://comingProjectsListView") # Data URL
        return r.text

def bs4Soup(html):
    soup = BeautifulSoup(html, 'lxml')
    html_list = soup.find_all('span')
    list1 = []
    dicct = {}
    for i in html_list:
        list = re.findall(r'[А-я]+|[0-9]+', i.text)
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
    amount = 0
    for key in dicct:
        dicct[key] = int(dicct[key])
        amount += dicct[key]
        print(key + "  -  " + str(dicct[key]))
        print(key.replace("СПБ", "").replace('МЕД', '').replace("Очередь", '').replace('проекта', '')\
                  .replace('1', '').replace('2', '').replace('3', '').strip() + "  -  " + str(dicct[key]))
        string += key.replace("СПБ", "").replace('МЕД', '').replace("медицинская", "мед.").replace("Консультация", "Конс.").replace("приложению", "прил.").replace("Очередь", '').replace('проекта', '')\
                  .replace('1', '').replace('2', '').replace('3', '').strip() + "  -  " + str(dicct[key]) + "\n"
    return  "\n" + string + "\n" + "Всего   -   " + str(amount)

def main():
    url = "http:///"
    bs4Soup(get_html(url))

def Draw():
    global text
    frame=tk.Frame(window,width=1000,height=1000,bd=1,bg ='#a9aeb0')
    frame.place(relx=.5, rely=.5, anchor="center")
    text=tk.Label(frame,text='')
    text.pack()

def Refresher():
    url = "http:///"
    global text
    text.configure(text=bs4Soup(get_html(url)), font=("Arial", 60, "bold"), fg="black", bg="#a9aeb0")
    window.after(5000, Refresher) # every second...

window = tk.Tk()
window.title("")
window.geometry("518x170")
window.configure(background='#a9aeb0')
#window.wm_attributes('-fullscreen', True) # Windows
window.attributes('-zoomed', True)

Draw()
Refresher()
window.mainloop()

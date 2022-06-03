from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
import re
import requests
from bs4 import BeautifulSoup

def RunGraphicUserInterface():
    def Tk_Quit(event=None):
        TkWindow.quit()
    
    TkWindow = Tk()
    TkWindow.title("I Know Baseball")
    TkWindow.geometry("+%d+%d" % (TkWindow.winfo_screenwidth()/2, TkWindow.winfo_screenheight()/2))
    TkWindow.resizable(False, False)
    TkWindow.bind('<Escape>', Tk_Quit)

    # 연도 선택 / 선수명 입력
    AddressBarSelectYearPlayerName = LabelFrame(text='경기 연도 / 선수명')
    AddressBarSelectYearPlayerName.pack(fill=BOTH, side=TOP)

    YearValues = [f'{i}년' for i in range(2014, 2022 + 1)]
    YearValues.append('전체')

    ComboboxSelectYear = Combobox(AddressBarSelectYearPlayerName, height=10, value=YearValues)
    ComboboxSelectYear.set("전체")
    ComboboxSelectYear.pack(side=LEFT)

    EntryPlayerName = Entry(AddressBarSelectYearPlayerName, width=22)
    EntryPlayerName.insert(0, '선수명 입력')
    EntryPlayerName.pack()

    # 팀 선택
    TeamValues = ['SSG', 'kt', '두산', '삼성', 'LG', '키움', 'NC', '롯데', 'KIA', '한화', '전체']

    AddressBarSelectTeam = LabelFrame(text='팀 선택')
    AddressBarSelectTeam.pack(fill=BOTH)

    ComboboxSelectLeftTeam = Combobox(AddressBarSelectTeam, height=10, value=TeamValues)
    ComboboxSelectLeftTeam.set("SSG")
    ComboboxSelectRightTeam = Combobox(AddressBarSelectTeam, height=10, value=TeamValues)
    ComboboxSelectRightTeam.set("전체")
    
    ComboboxSelectLeftTeam.pack(side=LEFT)
    ComboboxSelectRightTeam.pack(side=RIGHT)

    # 상황
    SituationValues = [
    '안타', '2루타', '3루타', '홈런', '1점홈런', '2점홈런', '3점홈런', '만루홈런', 
    '끝내기', '타점', '삼진', '볼넷', '사구', '희타', '병살'
    ]

    AddressBarSelectSituation = LabelFrame(text='상황')
    AddressBarSelectSituation.pack(fill=BOTH)

    ComboboxSelectSituation = Combobox(AddressBarSelectSituation, height=10, value=SituationValues)
    ComboboxSelectSituation.set("홈런")
    ComboboxSelectSituation.pack(side=LEFT)

    url_name = '최정'
    url_birth = None
    # statiz_url = f'http://www.statiz.co.kr/player.php?opt=6&sopt=0&name={url_name}&birth={url_birth}&re=0&da=0&year=1000&plist=&pdate='



    def RunSearch():
        print(EntryPlayerName.get())
        url_name = EntryPlayerName.get()
        if ComboboxSelectSituation.get() == '안타':
            url_situation = 2
        elif ComboboxSelectSituation.get() == '2루타':
            url_situation = 3
        elif ComboboxSelectSituation.get() == '3루타':
            url_situation = 4
        elif ComboboxSelectSituation.get() == '끝내기':
            url_situation = 0
        elif ComboboxSelectSituation.get() == '타점':
            url_situation = 6
        elif ComboboxSelectSituation.get() == '삼진':
            url_situation = 7
        elif ComboboxSelectSituation.get() == '볼넷':
            url_situation = 8
        elif ComboboxSelectSituation.get() == '희타':
            url_situation = 12
        elif ComboboxSelectSituation.get() == '병살':
            url_situation = 13
        else:
            url_situation = 5
        if ComboboxSelectYear.get() == '전체':
            url_year = '1000'
        else:
            url_year = re.search('\d{4}', ComboboxSelectYear.get()).group()

        statiz_url = f'http://www.statiz.co.kr/player.php?opt=6&sopt=0&name={url_name}&re=0&da={url_situation}&year={url_year}&plist=&pdate='

        if url_name:
            print(statiz_url)
            r = requests.get(statiz_url)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, features='lxml')
            oddrow_elms = soup.find_all(class_=re.compile(r'^oddrow_stz'))
            evenrow_elms = soup.find_all(class_=re.compile(r'^evenrow_stz'))

            for elm in oddrow_elms:
                game_date = re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group()
                print(game_date)
            for elm in evenrow_elms:
                game_date = re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group()
                print(game_date)

    ButtonSearch = Button(AddressBarSelectSituation, command=RunSearch, text='검색')
    ButtonSearch.pack()

    # 출력
    AddressBarResult = LabelFrame(text='검색 결과')
    AddressBarResult.pack(fill=BOTH, side=BOTTOM)

    ListboxResult = Listbox(AddressBarResult, width=45, selectmode=SINGLE)
    ListboxResult.pack(side=TOP)

    def OpenHighright():
        pass

    ButtonOpenHighright = Button(AddressBarResult, command=OpenHighright, text='선택일자 하이라이트 영상')
    ButtonOpenHighright.pack(side=BOTTOM)

    TkWindow.mainloop()

RunGraphicUserInterface()
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import *
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import webbrowser


Highright_link = []
Highright_count = 0

def RunGraphicUserInterface():
    def Tk_Quit(event=None):
        TkWindow.quit()
    
    TkWindow = Tk()
    TkWindow.title("I Know Baseball")
    TkWindow.geometry("+%d+%d" % (TkWindow.winfo_screenwidth()/2, TkWindow.winfo_screenheight()/2))
    TkWindow.resizable(False, False)
    TkWindow.bind('<Escape>', Tk_Quit)






    # 연도 선택 / 팀 선택 / 선수명 입력
    AddressBarSelectYearPlayerName = LabelFrame(text='경기 연도 / 상대팀 선택 / 선수명')
    AddressBarSelectYearPlayerName.pack(fill=BOTH, side=TOP)

    YearValues = [f'{i}년' for i in range(2014, 2022 + 1)]
    YearValues.append('전체')

    ComboboxSelectYear = Combobox(AddressBarSelectYearPlayerName, height=10, value=YearValues)
    ComboboxSelectYear.set("전체")
    ComboboxSelectYear.pack(side=LEFT)



    TeamValues = ['SSG', 'kt', '두산', '삼성', 'LG', '키움', 'NC', '롯데', 'KIA', '한화', '전체']

    ComboboxSelectRightTeam = Combobox(AddressBarSelectYearPlayerName, height=10, value=TeamValues)
    ComboboxSelectRightTeam.set("전체")
    
    ComboboxSelectRightTeam.pack(side=LEFT)


    EntryPlayerName = Entry(AddressBarSelectYearPlayerName, width=22)
    EntryPlayerName.insert(0, '선수명 입력')
    EntryPlayerName.pack()



    # 출력
    AddressBarResult = LabelFrame(text='검색 결과')
    AddressBarResult.pack(fill=BOTH, side=BOTTOM)

    ListboxResult = Listbox(AddressBarResult, width=69, selectmode=SINGLE)
    ListboxResult.pack(side=TOP)

    def CreateHighrightLink(year, home_team, away_team):
        def TranslationTeamName(team_name):
            if team_name == 'SSG' or team_name == 'SK':
                return 'SK'
            elif team_name == 'kt' or team_name == 'KT':
                return 'KT'
            elif team_name == '두산':
                return 'OB'
            elif team_name == '삼성':
                return 'SS'
            elif team_name == 'LG':
                return 'LG'
            elif team_name == '키움' or team_name == '넥센':
                return 'WO'
            elif team_name == 'NC':
                return 'NC'
            elif team_name == '롯데':
                return 'LT'
            elif team_name == 'KIA':
                return 'HT'
            elif team_name == '한화':
                return 'HH'
            elif team_name == None:
                print('???')
                return None
    
        link_year = year.split('-')
        link_year = ''.join(link_year)
        if (link_year[0:4] >= '2016'):
            return f'https://m.sports.naver.com/game/{link_year}{TranslationTeamName(away_team)}{TranslationTeamName(home_team)}0{link_year[0:4]}/video'
        return f'https://m.sports.naver.com/game/{link_year}{TranslationTeamName(away_team)}{TranslationTeamName(home_team)}0/video'

    def OpenHighright():
        webbrowser.open(Highright_link[ListboxResult.curselection()[0]])

    ButtonOpenHighright = Button(AddressBarResult, command=OpenHighright, text='선택일자 하이라이트 영상')
    ButtonOpenHighright.pack(side=BOTTOM)




    # 상황
    SituationValues = [
    '안타', '2루타', '3루타', '홈런', '1점홈런', '2점홈런', '3점홈런', '만루홈런', 
    '타점', '삼진', '볼넷', '사구', '희타', '병살'
    ]

    AddressBarSelectSituation = LabelFrame(text='상황')
    AddressBarSelectSituation.pack(fill=BOTH)

    ComboboxSelectSituation = Combobox(AddressBarSelectSituation, height=10, value=SituationValues)
    ComboboxSelectSituation.set("홈런")
    ComboboxSelectSituation.pack(side=LEFT)

    def RunSearch():
        global Highright_count

        ListboxResult.delete(0, Highright_count)
        Highright_count = 0
        Highright_link.clear()

        url_name = EntryPlayerName.get()
        if ComboboxSelectSituation.get() == '안타':
            url_situation = 2
        elif ComboboxSelectSituation.get() == '2루타':
            url_situation = 3
        elif ComboboxSelectSituation.get() == '3루타':
            url_situation = 4
        elif ComboboxSelectSituation.get() == '홈런':
            url_situation = 5
        elif ComboboxSelectSituation.get() == '1점홈런':
            url_situation = 5
        elif ComboboxSelectSituation.get() == '2점홈런':
            url_situation = 5
        elif ComboboxSelectSituation.get() == '3점홈런':
            url_situation = 5
        elif ComboboxSelectSituation.get() == '만루홈런':
            url_situation = 5
        elif ComboboxSelectSituation.get() == '타점':
            url_situation = 6
        elif ComboboxSelectSituation.get() == '삼진':
            url_situation = 7
        elif ComboboxSelectSituation.get() == '볼넷':
            url_situation = 8
        elif ComboboxSelectSituation.get() == '사구':
            url_situation = 9
        elif ComboboxSelectSituation.get() == '희타':
            url_situation = 12
        elif ComboboxSelectSituation.get() == '병살':
            url_situation = 13
        else:
            url_situation = 0
        if ComboboxSelectYear.get() == '전체':
            url_year = '1000'
        else:
            url_year = re.search('\d{4}', ComboboxSelectYear.get()).group()

        statiz_url = f'http://www.statiz.co.kr/player.php?opt=6&sopt=0&name={url_name}&re=0&da={url_situation}&year={url_year}&plist=&pdate='

        if url_name:
            r = requests.get(statiz_url)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, features='lxml')
            oddrow_elms = soup.find_all(class_=re.compile(r'^oddrow_stz'))
            evenrow_elms = soup.find_all(class_=re.compile(r'^evenrow_stz'))
            player_team = soup.find(class_=re.compile(r'^callout')).text
            player_team = re.search('최근 소속 (SSG|SK|kt|두산|삼성|LG|키움|넥센|NC|롯데|KIA|한화)', player_team).group()
            player_team = player_team[6:]
            
            elms = []
            elms_count = 0
            full_count = len(oddrow_elms) + len(evenrow_elms)
            while not elms_count == full_count:
                elms_count += 1
                if elms_count % 2 == 1:
                    elms.append(oddrow_elms.pop(0))
                if elms_count % 2 == 0:
                    elms.append(evenrow_elms.pop(0))


            for elm in elms:
                selected_team = None
                if not ComboboxSelectRightTeam.get() == '전체':
                    selected_team = ComboboxSelectRightTeam.get()

                selected_year = None
                if not ComboboxSelectYear.get() == '전체':
                    selected_year = ComboboxSelectYear.get()
                    selected_year = selected_year[:-1]
                
                td_elm = elm.find_all('td')
                elm_team = td_elm[1].text
                if elm_team == 'SK':
                    elm_team = 'SSG'
                elif elm_team == '넥센':
                    elm_team = '키움'

                if (selected_team == None or elm_team == selected_team) and (selected_year == None or re.search('\d{4}', elm.a['href']).group() == selected_year):
                    Highright_count += 1
                    game_date = re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group()
                    
                    if url_situation == 5:
                        if ComboboxSelectSituation.get() == '만루홈런' and (re.search('만루', td_elm[7].text)):
                            ListboxResult.insert(Highright_count, f'{game_date}  vs {td_elm[1].text}전 {td_elm[3].text}상대 {td_elm[2].text}, {td_elm[7].text}상황 {td_elm[6].text}')
                            if td_elm[2].text[-1] == '말':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), player_team, elm_team))
                            elif td_elm[2].text[-1] == '초':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), elm_team, player_team))

                        elif ComboboxSelectSituation.get() == '3점홈런' and (re.search('1,2루', td_elm[7].text) or re.search('1,3루', td_elm[7].text) or re.search('2,3루', td_elm[7].text)):
                            ListboxResult.insert(Highright_count, f'{game_date}  vs {td_elm[1].text}전 {td_elm[3].text}상대 {td_elm[2].text}, {td_elm[7].text}상황 {td_elm[6].text}')
                            if td_elm[2].text[-1] == '말':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), player_team, elm_team))
                            elif td_elm[2].text[-1] == '초':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), elm_team, player_team))
                            
                        elif ComboboxSelectSituation.get() == '2점홈런' and not re.search('1,2루', td_elm[7].text) \
                            and not re.search('1,3루', td_elm[7].text) and not re.search('2,3루', td_elm[7].text) \
                            and (re.search('1루', td_elm[7].text) or re.search('2루', td_elm[7].text) or re.search('3루', td_elm[7].text)):
                            ListboxResult.insert(Highright_count, f'{game_date}  vs {td_elm[1].text}전 {td_elm[3].text}상대 {td_elm[2].text}, {td_elm[7].text}상황 {td_elm[6].text}')
                            if td_elm[2].text[-1] == '말':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), player_team, elm_team))
                            elif td_elm[2].text[-1] == '초':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), elm_team, player_team))

                        elif ComboboxSelectSituation.get() == '1점홈런' and not re.search('1루', td_elm[7].text) and not re.search('2루', td_elm[7].text) and not re.search('3루', td_elm[7].text):
                            ListboxResult.insert(Highright_count, f'{game_date}  vs {td_elm[1].text}전 {td_elm[3].text}상대 {td_elm[2].text}, {td_elm[7].text}상황 {td_elm[6].text}')
                            if td_elm[2].text[-1] == '말':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), player_team, elm_team))
                            elif td_elm[2].text[-1] == '초':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), elm_team, player_team))

                        elif ComboboxSelectSituation.get() == '홈런':
                            ListboxResult.insert(Highright_count, f'{game_date}  vs {td_elm[1].text}전 {td_elm[3].text}상대 {td_elm[2].text}, {td_elm[7].text}상황 {td_elm[6].text}')
                            if td_elm[2].text[-1] == '말':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), player_team, elm_team))
                            elif td_elm[2].text[-1] == '초':
                                Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), elm_team, player_team))
                        continue
                    else:
                        ListboxResult.insert(Highright_count, f'{game_date}  vs {td_elm[1].text}전 {td_elm[3].text}상대 {td_elm[2].text}, {td_elm[7].text}상황 {td_elm[6].text}')
                        if td_elm[2].text[-1] == '말':
                            Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), player_team, elm_team))
                        elif td_elm[2].text[-1] == '초':
                            Highright_link.insert(Highright_count, CreateHighrightLink(re.search('\d{4}-\d{2}-\d{2}', elm.a['href']).group(), elm_team, player_team))



    ButtonSearch = Button(AddressBarSelectSituation, command=RunSearch, text='검색')
    ButtonSearch.pack()

    TkWindow.mainloop()

RunGraphicUserInterface()
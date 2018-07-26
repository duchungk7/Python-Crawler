#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- author: Mark Pei -*-

#import library
import re
import time
import tkinter
import requests
import threading
import webbrowser
import pandas as pd

from tkinter import ttk
from tkinter import messagebox
#from tkinter.font import Font
from bs4 import BeautifulSoup

#========= 全 域 變 數 宣 告 ===========
#global 
#save length df_output
ln = 0

#var for select keyword
keywords = 'TUL'
    
#var for select website
websites = 'https://www.mobile01.com/'

#save output title and web-links
df = pd.DataFrame(columns=['Title','Website', 'HREF'])
df_output = pd.DataFrame(columns=['Title','Website', 'HREF'])    

#save double-click links and title
df_click = pd.DataFrame(columns=['Title','Website', 'HREF', 'CLICKTIME','RESULT']) 

# update time after click
update_time = 300
#process df_click dataframe

#save click time
tStart = 0

#var for auto check click time
checkTime = 60.0
#======================================
#Use for calc click time, and change title color
def setTimer(str):
    global df_click
    ln_dfc = len(df_click.index)
        
    if ln_dfc > 0:
        tEnd = time.time()#stop timer
        #index_value = 0
        
        clktime0 = (int)(tEnd - df_click['CLICKTIME'][0])
        print("clk_time0: %f sec" % clktime0)
        if clktime0 > update_time:
            df_click.drop(df_click.index[0], inplace=True)
        
        #reset index
        df_click = df_click.reset_index(drop=True)   
        
    t = threading.Timer(checkTime, setTimer,[str])
    t.start()
    print(df_click)


#======================================
    
class simpleapp_TUL(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.menu()
        self.CrawlerGUI()
    
    def menu(self):
        #actions
        def Open():
            messagebox.showinfo("Open", "...")
        def Save():
            messagebox.showinfo("Save", "...")
        def Exit():
            #messagebox.askquestion("Question", "Are you sure to quit?")
            if messagebox.askokcancel("Question", "Are you sure to quit?"):
                self.destroy()
        def Cut():
            messagebox.showinfo("Cut", "...")
        def Copy():
            messagebox.showinfo("Copy", "...")
        def Paste():
            messagebox.showinfo("Paste", "...")
        def dialog():
            messagebox.showinfo("About", "Name: CRAWLER APPLICATION \nVersion: 1.0 \nDate: 2018/1/11 \nTUL DP760 Software Application Dept. ")
            
        menubar = tkinter.Menu(self)
        # create a pulldown menu, and add it to the menu bar
        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=Open)
        filemenu.add_command(label="Save", command=Save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=Exit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # create more pulldown menus
        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=Cut)
        editmenu.add_command(label="Copy", command=Copy)
        editmenu.add_command(label="Paste", command=Paste)
        menubar.add_cascade(label="Edit", menu=editmenu)
        
        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=dialog)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        # display the menu
        self.config(menu=menubar)
    
    
    def CrawlerGUI(self):
        self.grid()

        #ADD SPACE
        Label02 = tkinter.Label(self,text=u"  ")
        Label02.grid(column=0,row=1)  
        
        #SELECT KEYWORDS
        Label_keywords = tkinter.Label(self,
                                       text=u" SELECT KEYWORDS ",
                                       font=("Times New Roman",12, "bold"))
        Label_keywords.grid(column=0,row=2)
        
        #select keywords string
        self.box_value = tkinter.StringVar()
        self.box_key = ttk.Combobox(self.parent,
                                    textvariable=self.box_value,
                                    state='readonly',
                                    width='25')
        self.box_key['values'] = ('TUL', 'POWERCOLOR', 'AMD', '撼訊', '顯示卡', '顯卡', '外接顯卡',
                              '新驅動程式', '驅動程式', '挖礦', 'MINING', 'ETH','以太幣')
        
        #resPCD.encoding = 'big5'
        self.box_key.current(0)
        self.box_key.grid(column=0, row=4)
        
        #READ SELECT KEYWORD
        #call getKeywords function
        self.box_key.bind("<<ComboboxSelected>>", self.getKeywords)
        
        #ADD SPACE
        Label03 = tkinter.Label(self,text=u"     ")
        Label03.grid(column=1,row=2)
        Label04 = tkinter.Label(self,text=u"     ")
        Label04.grid(column=2,row=2)
        
        #SELECT WEBSITE
        label_web = tkinter.Label(self,
                                  text=u" SELECT WEBSITE ",
                                  font=("Times New Roman", 12, "bold"))
        label_web.grid(column=3,row=2)
        
        #select keywords string
        self.box_value2 = tkinter.StringVar()
        self.box_web = ttk.Combobox(self.parent,
                                    textvariable=self.box_value2,
                                    state='readonly',
                                    width = '25')
        self.box_web['values'] = ('https://www.mobile01.com/',
                                  'http://www.xfastest.com/',
                                  'https://www.pcdvd.com.tw/',
                                  'https://www.ptt.cc')
        self.box_web.current(0)
        self.box_web.grid(column=3, row=4)
        
        #read select ketwords
        #call getWebLink function
        self.box_web.bind("<<ComboboxSelected>>", self.getWebLink)
        
        #ADD SPACE
        Label05 = tkinter.Label(self,text=u"     ")
        Label05.grid(column=0,row=5)
        Label06 = tkinter.Label(self,text=u"     ")
        Label06.grid(column=0,row=6)
        
        #RUN button
        #Call crawlerProgram function
        btn_run = tkinter.Button(self,text=u" RUN ", width='25',
                                 font=("Times New Roman", 12, "bold"),
                                 command=self.crawlerProgram)
        btn_run.grid(column=0,row=7, columnspan=5, rowspan=1) 
        
        #add space
        Label07 = tkinter.Label(self,text=u"     ")
        Label07.grid(column=0,row=8)
        Label08 = tkinter.Label(self,text=u"     ")
        Label08.grid(column=0,row=9)
        Label09 = tkinter.Label(self,text=u"     ")
        Label09.grid(column=0,row=10)
        
        #RESULTS
        Label_result = tkinter.Label(self,
                                     text=u"RESULTS : ",
                                     font=("Times New Roman", 12, "bold"))
        Label_result.grid(column=0,row=11, columnspan=5, rowspan=1)
        #==========================================================
        
        #RESULTS ListBox
        listbox1 = tkinter.Listbox(self, height=20, width=90, fg = "blue")
        listbox1.grid(column=0,row=12, columnspan=5, rowspan=5, padx=5, pady=5)
        #listbox1.insert(0, "Open mobile web !")
        
        # create a vertical scrollbar to the right of the listbox
        yscroll = tkinter.Scrollbar(command=listbox1.yview, orient=tkinter.VERTICAL)
        yscroll.grid(column=5, row=12, columnspan=5, rowspan=5, sticky=tkinter.N+tkinter.S)
        listbox1.configure(yscrollcommand=yscroll.set)
        
        #label = tkinter.Label
        label_noted = tkinter.Label(self,text=u"*Note: Click title connect to website ! ", 
                                    font=("Times New Roman", 10))
        label_noted.grid(column=0,row=20)
        
        
        #Terminal ListBox
        text_box = tkinter.Text(self, height=5, width=90, bg='white', font=("Times New Roman", 10), state=tkinter.DISABLED)
        text_box.grid(column=0,row=19, columnspan=5, rowspan=5, padx=5, pady=5)
        
        # create a vertical scrollbar to the right of the listbox
        yscroll_tb = tkinter.Scrollbar(command=text_box.yview, orient=tkinter.VERTICAL)
        yscroll_tb.grid(column=5, row=19, columnspan=5, rowspan=5, sticky=tkinter.N+tkinter.S)
        text_box.configure(yscrollcommand=yscroll_tb.set)
        
        
    #========================== Action Function ==============================
    
    #Read Keywords from box_key and save at "keywords"
    def getKeywords(self, event):
        global keywords
        global write
        self.value_of_combo = self.box_key.get()
        keywords = self.value_of_combo
        #print(keywords)
        
    #Read web links from box_web and save at "web_links"
    def getWebLink(self, event):
        global websites
        global write
        self.value_of_combo = self.box_web.get()
        websites = self.value_of_combo
        #print(websites)
        
    
     
    #click RUN Button 
    def crawlerProgram(self):
        
        global keywords, websites
        
        global df
        global df_output
        global ln
        
        ln_df = len(df.index)
        
        #clear all DataFrame content
        df.drop(df.index[:ln_df], inplace=True)
        df_output.drop(df_output.index[:ln], inplace=True)

        #Click ListBox title, connect to website
        def connectToWebsite(event):
            global df_output, df_click
            global tStart 
            widget = event.widget
            selection=widget.curselection()
            #print(type(selection))
            #print(selection)
            
            #if click connect to webside, then listbox select change color
            slt = selection[0]
            listbox1.itemconfig(slt, fg='black')
            #listbox1.itemconfig(slt, bg='red', fg='black')
            length_df = len(df_output.index)
            
            lst = []
            for ix in range(length_df):
                lst.append(ix)
                #print(df_output['Website'][ix])
                if ix in selection:
                    webbrowser.open_new(df_output['Website'][ix])
                    tStart = time.time() #start timer
                    print("tStart time: %f " % tStart) 
                    df_click = df_click.append({'Title': df_output['Title'][ix],
                                                'Website': df_output['Website'][ix],
                                                'HREF':df_output['HREF'][ix], 'CLICKTIME':tStart }, ignore_index=True)
            print(df_click)
                    #print("ix in selection: " + ix)
                    
                           
        if websites == 'https://www.mobile01.com/':
            print("Select website mobile01.com")
            
            #===================================
            #crawler code in here
            res = requests.get("https://www.mobile01.com/forumtopic.php?c=17&s=7")
            #print (res.text)
            
            soup = BeautifulSoup(res.text,'html.parser')
            #print (soup.title.string)
            
            #titles = pd.Series()
            for title in soup.select("a[class='topic_gen']"):
                #titles = titles.append({'Title': title.string}).reset_index(drop=True)  #加到pd.Series
                df = df.append({'Title': title.string,
                                'Website': websites+title['href'],
                                'HREF':title['href']}, ignore_index=True)
                
                #find keyword in title
                for i in re.finditer(keywords, title.string):
                    df_output = df_output.append({'Title': title.string,
                                                  'Website': websites+title['href'],
                                                  'HREF':title['href']}, ignore_index=True)
                    break
            
            
            
            #check keywords in subweb (30 links)
            for i in range(5):
                sub_Title = df["Title"][i]
                sub_web_link = websites+df["HREF"][i]
                #print(sub_web_link)
                    
                #import requests
                subres = requests.get(sub_web_link)
                #print (subres.text)
                
                #from bs4 import BeautifulSoup
                sub_soup = BeautifulSoup(subres.text,'html.parser')
                #print (soup.title.string)
                
                #<div class="single-post-content">
                post_content = sub_soup.select("div[class='single-post-content']")
                #print(type(post_content))
                
                #write content to string
                content = " ".join(str(x) for x in post_content)
                #print(content)
               
                #find all keyword word
                for key in re.finditer(keywords, content):
                    #check title
                    #if the title is diferent, then write to [df_output]
                    check = 0
                    for daf in df_output['Title']:
                        #print("df['Title'][i] : " + sub_Title)
                        #print("daf : " + daf)
                        if sub_Title == daf:
                            check = 1
                            #break
                    if check ==1:
                        print("Found and saved")
                    else:
                        df_output = df_output.append({'Title': df['Title'][i],
                                                      'Website': websites+df['HREF'][i],
                                                      'HREF':df['HREF'][i]}, ignore_index=True)
                        # found keword, break out
                        break
                        
            
            #print(df_output)
            
        #print("==============================")
        if websites == 'http://www.xfastest.com/':
            print("Select website xfastest.com")
            #clear all DataFrame content
            #df_output.drop(df_output.index[:ln], inplace=True)
            #===================================
            #import requests
            resXfast = requests.get("http://www.xfastest.com/plugin.php?id=comeing_guide&type=newthread")
            #print (res.text)

            #from bs4 import BeautifulSoup
            soupXfast = BeautifulSoup(resXfast.text,'html.parser')
            #print (soup.title.string)
            
            #titles = pd.Series()
            for sel in soupXfast.select("h3 > a"):
                df = df.append({'Title': sel['title'], 'Website': sel['href']}, ignore_index=True)
                
                #find keyword in title
                for i in re.finditer(keywords, sel['title']):
                    df_output = df_output.append({'Title': sel['title'], 'Website': sel['href']}, ignore_index=True)
                    break
    

            #print(df)
            
            #check keywords in subweb (30 links)
            for i in range(5):
                sub_TitleX = df["Title"][i]
                sub_web_linkX = df["Website"][i]
                #print(df["Website"][i])
                
                #import requests
                subresX = requests.get(sub_web_linkX)
                #print (subresX.text)
                
                #from bs4 import BeautifulSoup
                sub_soupX = BeautifulSoup(subresX.text,'html.parser')
                #print (soup.title.string)
                
                #<td class="t_f" id="postmessage_797186">
                post_contentX = sub_soupX.select("td[class='t_f']")
                #print(type(post_contentX))
                
                #write content to string
                contentX = " ".join(str(x) for x in post_contentX)
                #print("======================================================")
                
                #find and check all keyword
                for keyX in re.finditer(keywords, contentX):
                    #check title
                    #if the title is diferent, then write to [df_output]
                    check = 0
                    for daf in df_output['Title']:
                        if sub_TitleX == daf:
                            check = 1
                            #break
                    if check ==1:
                        print("Found and saved")
                    else:
                        df_output = df_output.append({'Title': df['Title'][i], 'Website': sub_web_linkX}, ignore_index=True)
                    # found keword, break out
                    break
            
            #  THE END
            #OUTPUT : df_output
            
        if websites == 'https://www.pcdvd.com.tw/':
            print("Select website pcdvd.com")
            #clear all DataFrame content
            #df_output.drop(df_output.index[:ln], inplace=True)
            #================================
            
            #import requests
            resPCD = requests.get("https://www.pcdvd.com.tw/forumdisplay.php?f=8")
            #print (res.text)
            resPCD.encoding = 'big5'
            
            soupPCD = BeautifulSoup(resPCD.text,'html.parser')
            
            # GET title
            for selPCD in soupPCD.select("td[class='alt1Active'] > div > a"):
                #titles = titles.append({'Title': title.string}).reset_index(drop=True)  #加到pd.Series
                df = df.append({'Title': selPCD.text, 'Website': websites+selPCD['href']}, ignore_index=True)
                
                #find keyword in title
                for i in re.finditer(keywords, selPCD.text):
                    df_output = df_output.append({'Title': selPCD.text, 'Website': websites+selPCD['href']}, ignore_index=True)
                    break
            
            #==================================
            #check keywords in subweb (30 links)
            for i in range(5):
                sub_Title = df["Title"][i]
                sub_web_link = df["Website"][i]
                #print(df["Website"][i])
                
                #import requests
                subres = requests.get(sub_web_link)
                subres.encoding = 'big5'
                #print (subres.text)
                
                #from bs4 import BeautifulSoup
                sub_soup = BeautifulSoup(subres.text,'html.parser')
                #print (soup.title.string)
                
                #<td class="alt2" style="border-bottom: 1px solid #3A6EA5;">
                #<font size="2"><div>
                post_content = sub_soup.select("td > font")
                #post_content2 = sub_soup.select("td[class='alt1'] > font > div")
                filtered = [ v for v in str(post_content) if v[0] not in [u'/', u'>', u'<', u';', u'"'] and v[:2] not in [u'--'] ]
                filtered = [_f for _f in filtered if _f]  # remove empty strings
                
                #write content to string
                content = ''.join(filtered)
                content = re.sub(r'(\s)+', ' ', content)
                #content = " ".join(str(x) for x in post_content)
                #content = " ".join(str(x) for x in post_content2)
                
                #print(content)
                #print("======================================================")
                
                # find and check keyword
                #import re
                for key in re.finditer(keywords, content):
                    #check title
                    #if the title is diferent, then write to [df_output]
                    check = 0
                    for daf in df_output['Title']:
                        if sub_Title == daf:
                            check = 1
                            #break
                    if check ==1:
                        print("Found and saved")
                    else:
                        df_output = df_output.append({'Title': df['Title'][i], 'Website': sub_web_link}, ignore_index=True)
                        # found keword, break out
                    break
            
            #THE END
            #OUTPUT : df_output
            
        if websites == 'https://www.ptt.cc':
            print("Select website ptt.cc")
            #clear all DataFrame content
            #df_output.drop(df_output.index[:ln], inplace=True)
            #=============================
            
            #import requests
            resPTT = requests.get("https://www.ptt.cc/bbs/VideoCard/index.html")
            #print (resPTT.text)

            #from bs4 import BeautifulSoup
            soupPTT = BeautifulSoup(resPTT.text,'html.parser')
            #print (soup.title.string)
            
            # GET title
            
            #titles = pd.Series()
            for selPTT in soupPTT.select("div[class='title'] > a"):
                #titles = titles.append({'Title': title.string}).reset_index(drop=True)  #加到pd.Series
                df = df.append({'Title': selPTT.text, 'Website': websites+selPTT['href']}, ignore_index=True)
                
                #找出有 Keyword 字串的 title
                for i in re.finditer(keywords, selPTT.text):
                    df_output = df_output.append({'Title': selPTT.text, 'Website': websites+selPTT['href']}, ignore_index=True)
                    break
            
            
            
            #check keywords in subweb (30 links)
            for i in range(5):
                sub_Title = df["Title"][i]
                sub_web_link = df["Website"][i]
                #print(df["Website"][i])
                
                #import requests
                subres = requests.get(sub_web_link)
                #print (subres.text)
                
                #from bs4 import BeautifulSoup
                sub_soup = BeautifulSoup(subres.text,'html.parser')
                #print (soup.title.string)
                
                #<div class="article-metaline">
                main_content = sub_soup.find(id="main-content")
                metas = main_content.select('div.article-metaline')
                
                author = ''
                title = ''
                date = ''
                if metas:
                    author = metas[0].select('span.article-meta-value')[0].string if metas[0].select('span.article-meta-value')[0] else author
                    title = metas[1].select('span.article-meta-value')[0].string if metas[1].select('span.article-meta-value')[0] else title
                    date = metas[2].select('span.article-meta-value')[0].string if metas[2].select('span.article-meta-value')[0] else date
                    
                    # remove meta nodes
                    for meta in metas:
                        meta.extract()
                    for meta in main_content.select('div.article-metaline-right'):
                        meta.extract()
                
                #remove and keep push nodes
                try:
                    ip = main_content.find(text=re.compile(u'※ 發信站:'))
                    ip = re.search('[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*', ip).group()
                except:
                    ip = "None"
                
    
                # filter content
                filtered = [ v for v in main_content.stripped_strings if v[0] not in [u'※', u'◆'] and v[:2] not in [u'--'] ]
                filtered = [_f for _f in filtered if _f]  # remove empty strings
                #filtered = [x for x in filtered if article_id not in x]  # remove last line containing the url of the article
                content = ' '.join(filtered)
                content = re.sub(r'(\s)+', ' ', content)
                #print("======================================================")
                
                #find and check keyword
                for key in re.finditer(keywords, content):
                    #check title
                    #if the title is diferent, then write to [df_output]
                    check = 0
                    for daf in df_output['Title']:
                        #print("df['Title'][i] : " + sub_Title)
                        #print("daf : " + daf)
                        if sub_Title == daf:
                            check = 1
                            #break
                    if check ==1:
                        print("Found and saved")
                    else:
                        df_output = df_output.append({'Title': df['Title'][i], 'Website': sub_web_link}, ignore_index=True)
                    
                    # found keword, break out
                    break
                
            
            #  THE END
            #OUTPUT : df_output
            
            
        #print(df_output)
        ln = len(df_output.index)
        #print("length of df_output in crawlerProgram: " + str(ln))    
            
        #RESULTS ListBox
        listbox1 = tkinter.Listbox(self, height=20, width=90, fg = "blue")
        listbox1.grid(column=0,row=12, columnspan=5, rowspan=5, padx=5, pady=5)
            
        if len(df_output.index) == 0:
            listbox1.insert(0, "Not found any result, please select other keywords or websites !")
        inx = 0
        inx2 = 1
        #output in listbox
        for dfo in df_output['Title']:
            print(dfo)
            title_output = str(inx2) + '. ' + dfo
            listbox1.insert(inx, title_output)
            #after click links, change text color
            for dfc in df_click['Title']:
                if dfc == dfo:
                    listbox1.itemconfig(inx, fg='black')
                    break
                #else:
                    #listbox1.itemconfig(inx, fg='blue')
            inx = inx + 1
            inx2 = inx2 + 1
            
            
        listbox1.bind("<Double-Button-1>", connectToWebsite)
        
        #listbox1.bind("<Double-Button-1>", self.callback)
            
        # create a vertical scrollbar to the right of the listbox
        yscroll = tkinter.Scrollbar(command=listbox1.yview, orient=tkinter.VERTICAL)
        yscroll.grid(column=5, row=12, columnspan=5, rowspan=5, sticky=tkinter.N+tkinter.S)
        listbox1.configure(yscrollcommand=yscroll.set)
            
        #crawler code in here
        #====================
        
            
if __name__ == "__main__":
    app = simpleapp_TUL(None)
    app.title('TUL CRAWLER APPLICATION')
    
    timer = threading.Timer(checkTime,setTimer,['clear df_click dataFrame !'])
    timer.start()
    
    #resize
    app.geometry("580x660")
    app.resizable(1,0) 
    
    app.mainloop()
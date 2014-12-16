#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PSIT Project: Note That
Developers: Adisorn Sripakpaisit
            Wisantoon jangwongwarus
"""
#---------------Import-----------------#
try:
    from Tkinter import *
except:
    from tkinter import *
from ScrolledText import ScrolledText
import sqlite3 as sql
import datetime
import tkMessageBox
#--------------------------------------#

def date():
    """
    Return current date
    """
    day = int(datetime.date.today().strftime("%d"))
    month = datetime.date.today().strftime("%B")
    year = datetime.date.today().strftime("%Y")
    date_now = "%s %s %s" % (day, month, year)
    return date_now

def add_data(title, text, datetime, favorite):
    """
    Add new data to database
    """
    new_data = [title, text, datetime, favorite]
    data = sql.connect('Database.db')
    data.text_factory = str
    cur = data.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS NoteStorage
                (Title text, Notedata text, DateTime text, Important text)''')
    cur.execute("INSERT INTO NoteStorage VALUES (?, ?, ?, ?)", new_data)
    data.commit()
    data.close()

def delete_data(title):
    """
    Delete select data in database
    """
    data = sql.connect("Database.db")
    cur = data.cursor()
    cur.execute("DELETE FROM NoteStorage WHERE Title = '%s'" % title)
    data.commit()
    data.close()

def get_data():
    """
    Return all data in database as a dict
    """
    all_data = {}
    data = sql.connect('Database.db')
    cur = data.cursor()
    try:
        cur.execute("SELECT * FROM NoteStorage ORDER BY Title")
        for i in cur:
            if i[0] not in all_data:
                all_data[i[0]] = []
            all_data[i[0]].append(i[1])
            all_data[i[0]].append(i[2])
            all_data[i[0]].append(i[3])
        return all_data
    except:
        add_data('new', 'new', 'new', '0')
        delete_data('new')
        cur.execute("SELECT * FROM NoteStorage ORDER BY Title")
        for i in cur:
            if i[0] not in all_data:
                all_data[i[0]] = []
            all_data[i[0]].append(i[1])
            all_data[i[0]].append(i[2])
            all_data[i[0]].append(i[3])
        return all_data
        

def get_favorite():
    '''
    Return all favorite note
    '''
    favor_data = {}
    data = sql.connect('Database.db')
    cur = data.cursor()
    all_data = cur.execute('SELECT * FROM NoteStorage ORDER BY Title')
    for i in all_data:
        if i[3] == '1':
            if i[0] not in favor_data:
                favor_data[i[0]] = []
            favor_data[i[0]].append(i[1])
            favor_data[i[0]].append(i[2])
            favor_data[i[0]].append(i[3])
    return favor_data
            

class Note(Toplevel):
    """
    Display select Note
    """

    def __init__(self, window=None, *args, **kwargs):
        Toplevel.__init__(self, window=None, *args, **kwargs)
        self.background = PhotoImage(file='Image/note_bg1.gif')
        self.image = PhotoImage(file='Image/favorite.gif')
        self.window = window

    def delete_select(self, title):
        """Delete data and destroy current window"""
        ask = tkMessageBox.askquestion("Delete", "Are you sure?", icon="warning")
        if ask == 'yes':
            delete_data(title)
            self.destroy()
            self.window.destroy()
            note_store = NoteStorage()
            note_store.geometry('450x600+450+90')
            note_store.title('Note Storage')
            note_store.resizable(width=False, height=False)
            note_store.all_note()

    def my_note(self, title):
        """
        Create UI for note
        """
        data = get_data()[title]

        self.bg = Label(self, image=self.background)
        self.header = Frame(self, bg='#FF8400', width=350, height=50)
        self.title = Label(self.header, text=title, bg='#FF8400', fg='white',
                           font=('AngsanaUPC', 24, 'bold'))
        self.txt = ScrolledText(self, width=47, height=13, bg='#FFECA5',\
                                font=('AngsanaUPC', 14), relief=FLAT)
        self.txt.insert('1.0', data[0])
        self.txt.config(state='disable')
        self.ok = Button(self, text='Ok', bg='#02d602', relief=FLAT,
                         width=10, fg='white', font=('Arial', 10, 'bold'),
                         command=self.destroy, activebackground='white',
                         activeforeground='#02d602')
        self.delete = Button(self, text='Delete', bg='red', relief=FLAT,
                             width=10, fg='white', font=('Arial', 10, 'bold'),
                             activebackground='white', activeforeground=
                             'red', command=lambda
                             title=title: self.delete_select(title))
        
        self.bg.place(x=-2, y=0)
        self.header.place(x=0, y=0)
        self.title.place(x=10, y=-1)
        self.ok.place(x=140, y=445)
        self.delete.place(x=235, y=445)
        self.txt.place(x=25, y=80)
        
        if data[2] == '1':
            self.favor = Label(self, image=self.image, bg='#FF8400')
            self.favor.place(x=286, y=-1)

class NoteStorage(Toplevel):
    """
    Note storage page
    """
    
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.papers = PhotoImage(file='Image/paper.gif')
        self.star = PhotoImage(file='Image/star.gif')
        self.storage = PhotoImage(file='Image/logo_Storage.gif')
        self.height = 120 * len(get_data())

    def all_note(self):
        """
        Display Main note storage page
        """
        self.header = Frame(self, height=60, width=450, bg='#009ffb')
        self.logo = Label(self.header, image=self.storage, bg='#009ffb')
        self.canvas = Canvas(self, width=450)
        self.frame = Frame(self.canvas, height=self.height, width=450)
        self.scr = Scrollbar(self.canvas, orient='vertical',
                             command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scr.set)
        self.header.pack()
        self.logo.place(x=125, y=7)
        self.canvas.pack(fill=BOTH, expand=True)
        self.scr.pack(side=RIGHT, fill=Y)
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW,
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.setting)
        self.bind("<MouseWheel>", self.wheel)
        self.list_note()

    def wheel(self, event):
        """
        scroll wheel
        """
        self.canvas.yview_scroll(-1*(event.delta/100), "units")

    def setting(self, event):
        """
        Config scrollbar react with canvas
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_page(self, title):
        """
        Open select note
        """
        page = Note(self)
        page.geometry('350x500+500+150')
        page.title('Title' + ' ' + '-' + ' ' + title)
        page.my_note(title)
        page.resizable(width=False, height=False)

    def list_note(self):
        """
        Display list of all note
        """
        count = 5
        num = 1
        data = sql.connect('Database.db')
        cur = data.cursor()
        cur.execute("SELECT * FROM NoteStorage")
        for i in cur:
            text = i[1].splitlines()[0]
            if len(text) > 30:
                text = text[:30] + '...'
            if num % 2 == 0: color = 'gray'
            else: color = 'white'
            
            self.back = LabelFrame(self.frame, bg=color, width=410, height=115)
            self.button = Button(self.frame, text=num, fg='white', bg='#ff8400',
                                 relief=FLAT, width=3,
                                 font=('Arial', 16, 'bold'),
                                 command=lambda i=i: self.open_page(i[0]))
            self.paper = Label(self.frame, image=self.papers, bg=color)
            self.title = Label(self.frame, text=i[0], bg='#fff6aa',
                               font=('AngsanaUPC', 15, 'bold'))
            self.text = Label(self.frame, text=text, bg='#fff6aa',
                              font=('AngsanaUPC', 12), justify=LEFT)
            self.date = Label(self.frame, text=i[2], bg='#fff6aa',
                              font=('AngsanaUPC', 12))
            if i[3] == '1':
                self.star_logo = Label(self.frame, image=self.star, bg='#fff6aa')
                self.star_logo.place(x=370, y=70+count)
                
            self.back.place(x=13, y=count)
            self.button.place(x=20, y=12+count)
            self.paper.place(x=75, y=10+count)
            self.title.place(x=90, y=12+count)
            self.text.place(x=95, y=50+count)
            self.date.place(x=315, y=12+count)
            count += 120
            num += 1
        data.close()
            

class Findpage(Toplevel):
    """
    Represent a Find page
    """
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.find_box()

    def find_box(self):
        """
        Main UI for find page
        """
        self.header = Frame(self, width=450, height=100, bg='gray')
        self.label = Label(self.header, text='Search', fg='white', bg='gray',\
                           font=('AngsanaUPC', 18, 'bold'))
        self.box = Entry(self.header, bg='white', font=('AngsanaUPC', 12),\
                         width=70)
        self.button1 = Button(self.header, text='Search', bg='white', width=10,\
                              relief=FLAT, command=self.list_note)
        self.button2 = Button(self.header, text='Cancel', bg='white', width=10,\
                              relief=FLAT, command=self.destroy)
        self.favor = Button(self.header, text='Favorite', relief=FLAT, width=10,\
                            bg='green', command=lambda: self.list_note(1))
        self.body = Frame(self, bg='white')
        self.list = Listbox(self.body, bg='white')
        self.body = Frame(self, bg='white')

        self.header.pack()
        self.label.place(x=175, y=0)
        self.box.place(x=20, y=35)
        self.button1.place(x=155, y=67)
        self.button2.place(x=255, y=67)
        self.favor.place(x=55, y=67)
        self.body.pack(fill=BOTH, expand=True)

    def list_note(self, num=0):
        """
        Display list of note
        """
        text = self.box.get()
        self.box.delete(0, END)
        self.list.destroy()
        self.list = Listbox(self.body, bg='white', relief=FLAT,\
                            font=('AngsanaUPC', 16),\
                            activestyle='none')
        
        self.scr = Scrollbar(self.list, orient=VERTICAL)
        self.list.config(yscrollcommand=self.scr.set)
        self.scr.config(command=self.list.yview)
        self.scr.pack(side=RIGHT, fill=Y)
        
        if num == 0:
            data = get_data()
        else:
            data = get_favorite()

        if text == '':
            for i in data:
                self.list.insert(END, i)
        else:
            for i in data:
                if text in i:
                    self.list.insert(END, i)

        self.list.pack(fill=BOTH, expand=True)
        self.list.bind("<Double-Button-1>", self.open_page)

    def open_page(self, event):
        """
        Open select note
        """
        widget = event.widget
        select = widget.curselection()
        value = widget.get(select[0])

        page = Note()
        page.geometry('350x500+500+150')
        page.title('Title' + ' ' + '-' + ' ' + value)
        page.my_note(value)
        page.resizable(width=False, height=False)


class Notepage(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.bg_page = PhotoImage(file="Image/bg_note.gif")
        self.favorite_logo = PhotoImage(file="Image/favorite.gif")

    def note_pages(self, text_title, text_note, favorite):
        """
        Display a Note when add new note or edit note
        """
        
        def add_destroy():
            """
            add new data and destroy current window
            """
            message = tkMessageBox.showinfo('Status', 'Complete')
            add_data(text_title, text_note, date(), favorite)
            self.destroy()
        
        #Background
        self.background = Label(self, image=self.bg_page)
        
        #header and title
        self.decorate = Frame(self, bg='#FF8400', width=350, height=50)
        self.new_note = Label(self.decorate, text=text_title,
                              bg='#FF8400', fg='white',
                              font=('AngsanaUPC', 24, 'bold'))

        #note
        self.txt = ScrolledText(self, width=47, height=13, bg='#FFECA5',\
                                font=('AngsanaUPC', 14), relief=FLAT)
        self.txt.insert('1.0', text_note)
        self.txt.config(state='disable')

        #Button
        self.ok = Button(self, text='Ok', bg='#02d602', relief=FLAT,
                         width=10, fg='white', font=('Arial', 10, 'bold'),
                         command=add_destroy, activebackground='white',
                         activeforeground='#02d602')
        self.cancel = Button(self, text='Cancel', bg='#a0a0a0', relief=FLAT,
                             width=10, fg='white', font=('Arial', 10, 'bold'),
                             activebackground='white', activeforeground=
                             '#a0a0a0', command=self.destroy)
        
        self.background.place(x=0, y=0)
        self.decorate.place(x=0, y=0)
        self.new_note.place(x=15, y=0)
        self.txt.place(x=25, y=80)
        self.ok.place(x=140, y=445)
        self.cancel.place(x=235, y=445)
        
        if favorite == 1:
            self.favor = Label(self, image=self.favorite_logo, bg='#FF8400')
            self.favor.place(x=286, y=-1)

class About(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.credit()

    def credit(self):
        """
        Main UI about page
        """
        self.frame = Frame(self, bg='#B7B7B7', width=250, height=100)
        self.name = Label(self, text='Note That', fg='white', bg='#B7B7B7',
                          font=('Arial', 30, 'bold'))
        self.label = Label(self, text='PSIT Project 2014'
                           , fg='white', bg='#B7B7B7', font=('Arial', 10, 'bold'))
        self.text1 = Label(self, text='Create by', font=('Arial', 16))
        self.text2 = Label(self, text='Adisorn  Sripakpaisit',
                           font=('Arial', 10))
        self.text3 = Label(self, text='Wisantoon Jangwongwarus',
                           font=('Arial', 10))
        self.text4 = Label(self, text='Faculty of Information Technology',
                           font=('Arial', 10))
        self.text4 = Label(self, text="King Mongkut's \n Institute of Technology Ladkrabang",
                           font=('Arial', 10))
        self.button = Button(self, text='Close', command=self.destroy)

        self.frame.place(x=0, y=0)
        self.name.place(x=35, y=10)
        self.label.place(x=65, y=65)
        self.text1.place(x=75, y=110)
        self.text2.place(x=60, y=150)
        self.text3.place(x=42, y=175)
        self.text4.place(x=25, y=220)
        self.text4.place(x=15, y=241)
        self.button.place(x=100, y=300)
        
class MainApp(Tk):
    """
    Represent a main page
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.find_b = PhotoImage(file="Image/Find_button.gif")
        self.date = date()
        self.var = IntVar()
        self.logo = PhotoImage(file='Image/logo_app.gif')

    def note_storage(self):
        """
        Create Note Storage page
        """
        note_store = NoteStorage()
        note_store.geometry('450x600+450+90')
        note_store.title('Note Storage')
        note_store.resizable(width=False, height=False)
        note_store.all_note()

    def create_note(self):
        """
        Create new note page
        """
        title_name = self.title_box.get()
        note_text = self.note_box.get('1.0', END)
        favorite = self.var.get()

        count = 0
        for i in get_data():
            if title_name == i:
                break
            else:
                count += 1
        
        if title_name != '' and note_text != '' and count == len(get_data()):
            self.title_box.delete(0, END)
            self.note_box.delete('1.0', END)
            note_page = Notepage()
            note_page.geometry('350x500+500+150')
            note_page.title('New note' + ' ' + ':' + ' ' + title_name)
            note_page.resizable(width=False, height=False)
            note_page.note_pages(title_name, note_text, favorite)
        elif title_name in get_data():
            error = tkMessageBox.showerror('Error', 'Duplicate title name!')

    def find_notes(self):
        """
        Create find note page
        """
        find = Findpage()
        find.geometry('400x500+475+145')
        find.resizable(width=False, height=False)
        find.title('Find your note')

    def window(self):
        """
        Display Main window
        """
        #Header#
        self.header = Frame(self, width=450, height=65, bg='#1E90FF')
        self.logo_name = Label(self.header, image=self.logo, bg='#1E90FF')
        self.datetime = Label(self, text=self.date)
        
        #Input#
        self.title_name = Label(self, text="Title", font=('Arial', 12,))
        self.title_box = Entry(self, width = 58, bg='white', relief=FLAT,  
                                font=('AngsanaUPC', 15))
        self.note_text = Label(self, text="Your Note", font=('Arial', 12,))
        self.note_box = ScrolledText(self, font=('AngsanaUPC', 14), width=65,
                                     relief=FLAT, bg='white', height=9)
        
        #Check list
        self.check = Checkbutton(self, text='Favorite', bg='#FEFF92',
                      variable=self.var, activebackground='#FEFF92',
                      width=55, justify='left')
        
        #Button#
        self.add_note = Button(self, width=45, text="Add Note", 
                               bg='green', relief=FLAT, font=('Arial', 11, 'bold')
                               , command=self.create_note, fg='white',
                               activeforeground='green')
        self.find_note = Button(self.header, image=self.find_b, relief=FLAT, 
                              bg='gray', font=('Arial', 13, 'bold')
                                , command=self.find_notes, width=68, height=59,
                                overrelief=RIDGE, activebackground='#1E90FF')
        self.all = Button(self, width=31, height=2, fg='white', 
                                text="Note Storage", bg='#009cff',
                                relief=FLAT, activeforeground='#009cff', 
                                font=('Arial', 16, 'bold'),
                          command=self.note_storage)

        #Footer#
        self.last = Frame(self, bg='#1E90FF', width=450, height=25)
        self.fac = Label(self.last, fg='white', bg='#1E90FF', 
                         text="Faculty of Information Technology, KMITL")

        self.header.place(x=0, y=0)
        self.logo_name.place(x=15, y=5)
        self.datetime.place(x=325, y=75)
        self.title_name.place(x=20, y=80)
        self.title_box.place(x=20, y=110)
        self.note_text.place(x=20, y=150)
        self.note_box.place(x=20, y=185)
        self.check.place(x=20, y=423)
        self.add_note.place(x=20, y=457)
        self.find_note.place(x=376, y=0)
        self.all.place(x=20, y=500)
        self.last.place(x=0, y=575)
        self.fac.place(x=110, y=3)

class Home(Tk):
    """
    Main window of home page
    """

    def __init__(self):
        Tk.__init__(self)
        self.back = PhotoImage(file='Image/background.gif')
        self.logo = PhotoImage(file='Image/main_logo.gif')
        self.note = PhotoImage(file='Image/note.gif')
        self.about = PhotoImage(file='Image/about.gif')
        self.exit = PhotoImage(file='Image/exit.gif')
        self.note_press = PhotoImage(file='Image/note2.gif')
        self.about_press = PhotoImage(file='Image/about2.gif')
        self.exit_press = PhotoImage(file='Image/exit2.gif')
        
    def main(self):
        """
        Open Main app
        """
        self.destroy()
        app = MainApp()
        app.resizable(width=False, height=False)
        app.title("Note That")
        app.geometry("450x600+450+90")
        app.window()
        app.mainloop()

    def credit(self):
        """
        Open About page
        """
        about = About()
        about.geometry('250x350+560+190')
        about.resizable(0, 0)
        about.title("About")

    def flat(self, event):
        """Event widget flat"""
        event.widget.config(relief=FLAT, activebackground='#f8f6f4')

    def press_note1(self, event):
        """Event when press button"""
        self.button1.config(image=self.note_press)

    def press_note2(self, event):
        """Event when release button"""
        self.button1.config(image=self.note)

    def press_about1(self, event):
        """Event when press button"""
        self.button2.config(image=self.about_press)

    def press_about2(self, event):
        """Event when release button"""
        self.button2.config(image=self.about)

    def press_exit1(self, event):
        """Event when press button"""
        self.button3.config(image=self.exit_press)

    def press_exit2(self, event):
        """Event when release button"""
        self.button3.config(image=self.exit)

    def welcome(self):
        """
        Main UI
        """
        self.bg = Label(self, image=self.back)
        self.logo_name = Label(self, image=self.logo, bg='#f8f6f4')
        self.button1 = Button(self, image=self.note, bg='#f8f6f4', relief=FLAT,
                              command=self.main)
        self.button2 = Button(self, image=self.about, bg='#f8f6f4', relief=FLAT,
                              command=self.credit)
        self.button3 = Button(self, image=self.exit, bg='#f8f6f4', relief=FLAT,
                              command=self.destroy)

        self.bg.place(x=-2, y=-2)
        self.logo_name.place(x=50, y=90)
        self.button1.place(x=60, y=210)
        self.button2.place(x=60, y=310)
        self.button3.place(x=60, y=410)
        
        self.bind("<Button-1>", self.flat)
        self.button1.bind("<Button-1>", self.press_note1)
        self.button1.bind("<ButtonRelease-1>", self.press_note2)
        self.button2.bind("<Button-1>", self.press_about1)
        self.button2.bind("<ButtonRelease-1>", self.press_about2)
        self.button3.bind("<Button-1>", self.press_exit1)
        self.button3.bind("<ButtonRelease-1>", self.press_exit2)

        
if __name__ == "__main__":
    app = Home()
    app.resizable(width = False, height = False)
    app.title("Note That")
    app.geometry("450x600+450+90")
    app.welcome()
    app.mainloop()

    

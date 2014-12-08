# -*- coding: utf-8 -*-
from Tkinter import *
from ScrolledText import ScrolledText
import sqlite3 as sqlite
import datetime
import tkMessageBox

def date():
    """
    Return current time
    """
    day = int(datetime.date.today().strftime("%d"))
    month = datetime.date.today().strftime("%B")
    year = datetime.date.today().strftime("%Y")
    date_now = "%s %s %s" % (day, month, year)
    return date_now

def add_data(title, text, datetime, important):
    """
    Add new data to database
    """
    new_data = [title, text, datetime, important]
    data = sqlite.connect('Database.db')
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
    data = sqlite.connect("Database.db")
    cur = data.cursor()
    cur.execute("DELETE FROM NoteStorage WHERE Title = '%s'" % title)
    data.commit()
    data.close()

def get_data():
    """
    Return all data in database as a dict
    """
    all_data = {}
    data = sqlite.connect('Database.db')
    cur = data.cursor()
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
    data = sqlite.connect('Database.db')
    cur = data.cursor()
    all_data = cur.execute('SELECT * FROM NoteStorage ORDER BY Title')
    for i in all_date:
        if i[3] == '1':
            if i[0] not in favor_data:
                favor_data[i[0]] = []
            favor_data[i[0]].append(i[1])
            favor_data[i[0]].append(i[2])
            favor_data[i[0]].append(i[3])
    return favor_data
            

class Note(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.background = PhotoImage(file='note_bg1.gif')
        self.image = PhotoImage(file='favorite.gif')

    def delete_select(self, title):
            ask = tkMessageBox.askquestion("Delete", "Are you sure?", icon="warning")
            if ask == 'yes':
                delete_data(title)
                self.destroy()

    def my_note(self, title):
        """
        Create UI for note
        """
        data = get_data()[title]

        self.bg = Label(self, image=self.background)
        self.bg.place(x=0, y=0)

        self.header = Frame(self, bg='#FF8400', width=350, height=50)
        self.header.place(x=0, y=0)
        self.title = Label(self.header, text=title, bg='#FF8400', fg='white',
                           font=('AngsanaUPC', 24, 'bold'))
        self.title.place(x=10, y=-1)

        self.paper = Frame(self, width=300, height=350, bg='#FFECA5')
        self.paper.place(x=25, y=80)
        self.word = Label(self.paper, text=data[0], justify=LEFT,
                          font=('AngsanaUPC', 14), padx=10, pady=10,
                          bg='#FFECA5', wraplength=280)
        self.word.place(x=0, y=0)

        self.ok = Button(self, text='Ok', bg='#02d602', relief=FLAT,
                         width=10, fg='white', font=('Arial', 10, 'bold'),
                         command=self.destroy, activebackground='white',
                         activeforeground='#02d602')
        self.ok.place(x=140, y=445)
        self.delete = Button(self, text='Delete', bg='red', relief=FLAT,
                             width=10, fg='white', font=('Arial', 10, 'bold'),
                             activebackground='white', activeforeground=
                             'red', command=lambda
                             title=title: self.delete_select(title))
        self.delete.place(x=235, y=445)
        if data[2] == '1':
            self.favor = Label(self, image=self.image, bg='#FF8400')
            self.favor.place(x=286, y=-1)
        
   

class NoteStorage(Toplevel):
    
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.papers = PhotoImage(file='paper.gif')
        self.star = PhotoImage(file='star.gif')
        self.storage = PhotoImage(file='logo_Storage.gif')
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
        self.logo.place(x=10, y=7)
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
        page = Note()
        page.geometry('350x500+500+150')
        page.title('Title' + ' ' + '-' + ' ' + title)
        page.my_note(title)
        page.resizable(width=False, height=False)

    def list_note(self):
        """
        Display list of all note
        """
        count = 0
        num = 1
        data = get_data()
        for i in data:
            text = data[i][0].splitlines()[0]
            if len(text) > 40:
                text = text[:40] + '...'
            self.button = Button(self.frame, text=num, fg='white', bg='#ff8400',
                                 relief=FLAT, width=3,
                                 font=('Arial', 16, 'bold'),
                                 command=lambda i=i: self.open_page(i))
            self.paper = Label(self.frame, image=self.papers)
            self.title = Label(self.frame, text=i, bg='#fff6aa',
                               font=('AngsanaUPC', 15, 'bold'))
            self.text = Label(self.frame, text=text, bg='#fff6aa',
                              font=('AngsanaUPC', 12), justify=LEFT)
            self.date = Label(self.frame, text=data[i][1], bg='#fff6aa',
                              font=('AngsanaUPC', 12))
            if data[i][2] == '1':
                self.star_logo = Label(self.frame, image=self.star, bg='#fff6aa')
                self.star_logo.place(x=370, y=80+count)

            self.button.place(x=20, y=22+count)
            self.paper.place(x=75, y=20+count)
            self.title.place(x=90, y=22+count)
            self.text.place(x=95, y=60+count)
            self.date.place(x=315, y=20+count)
            count += 120
            num += 1


class Findpage(Toplevel):
    """
    Represent a Find page
    """
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.find_box()

    def find_box(self):
        self.header = Frame(self, width=450, height=100, bg='gray')
        self.label = Label(self.header, text='Search', fg='white', bg='gray',\
                           font=('AngsanaUPC', 18, 'bold'))
        self.box = Entry(self.header, bg='white', font=('AngsanaUPC', 12),\
                         width=70)
        self.button1 = Button(self.header, text='Search', bg='white', width=10,\
                              relief=FLAT, command=self.list_note)
        self.button2 = Button(self.header, text='Cancel', bg='white', width=10,\
                              relief=FLAT, command=self.destroy)
        self.body = Frame(self, bg='white')
        self.list = Listbox(self.body, bg='white')
        self.body = Frame(self, bg='white')

        self.header.pack()
        self.label.place(x=175, y=0)
        self.box.place(x=20, y=35)
        self.button1.place(x=120, y=67)
        self.button2.place(x=210, y=67)
        self.body.pack(fill=BOTH, expand=True)


class Notepage(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.bg_page = PhotoImage(file="bg_note.gif")
        self.favorite_logo = PhotoImage(file="favorite.gif")

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
        self.background.place(x=0, y=0)
        
        #header and title
        self.decorate = Frame(self, bg='#FF8400', width=350, height=50)
        self.decorate.place(x=0, y=0)
        self.new_note = Label(self.decorate, text=text_title,
                              bg='#FF8400', fg='white',
                              font=('AngsanaUPC', 24, 'bold'))
        self.new_note.place(x=15, y=0)

        #note
        self.paper = Frame(self, width=300, height=350, bg='#FFECA5')
        self.paper.place(x=25, y=80)
        self.word = Label(self.paper, text=text_note, justify=LEFT,
                          font=('AngsanaUPC', 14), padx=10, pady=10,
                          bg='#FFECA5', wraplength=280)
        self.word.place(x=0, y=0)

        #Button
        self.ok = Button(self, text='Ok', bg='#02d602', relief=FLAT,
                         width=10, fg='white', font=('Arial', 10, 'bold'),
                         command=add_destroy, activebackground='white',
                         activeforeground='#02d602')
        self.ok.place(x=140, y=445)
        self.cancel = Button(self, text='Cancel', bg='#a0a0a0', relief=FLAT,
                             width=10, fg='white', font=('Arial', 10, 'bold'),
                             activebackground='white', activeforeground=
                             '#a0a0a0', command=self.destroy)
        self.cancel.place(x=235, y=445)
        if favorite == 1:
            self.favor = Label(self, image=self.favorite_logo, bg='#FF8400')
            self.favor.place(x=286, y=-1)

class About(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        self.credit()

    def credit(self):
        self.frame = Frame(self, bg='#B7B7B7', width=250, height=100)
        self.frame.place(x=0, y=0)
        self.name = Label(self, text='Note That', fg='white', bg='#B7B7B7',
                          font=('Arial', 30, 'bold'))
        self.name.place(x=35, y=10)
        self.label = Label(self, text='PSIT Project 2014'
                           , fg='white', bg='#B7B7B7', font=('Arial', 10, 'bold'))
        self.label.place(x=65, y=65)
        
        
class MainApp(Tk):
    """
    Represent a main page
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.find_b = PhotoImage(file="Find_button.gif")
        self.date = date()
        self.var = IntVar()
        self.logo = PhotoImage(file='logo_app.gif')
        self.window()

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
        title_name = self.title_box.get().encode('utf-8')
        note_text = self.note_box.get('1.0', END).encode('utf-8')
        favorite = self.var.get()
        if title_name != '' and note_text != '' and title_name not in get_data():
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

    def credit(self):
        """
        Open about page
        """
        about = About()
        about.geometry('250x350+550+190')
        about.resizable(width=False, height=False)
        about.title('About')

    def window(self):
        """
        Display Main window
        """
        #Header#
        self.header = Frame(self, width=450, height=65, bg='#1E90FF')
        self.header.place(x=0, y=0)
        self.logo_name = Label(self.header, image=self.logo, bg='#1E90FF')
        self.logo_name.place(x=15, y=5)
        self.datetime = Label(self, text=self.date)
        self.datetime.place(x=325, y=75)

        #Input#
        self.title_name = Label(self, text="Title", font=('Arial', 12,))
        self.title_name.place(x=20, y=80)
        self.title_box = Entry(self, width = 58, bg='white', relief=FLAT,  
                                font=('AngsanaUPC', 15))
        self.title_box.place(x=20, y=110)

        self.note_text = Label(self, text="Your Note", font=('Arial', 12,))
        self.note_text.place(x=20, y=150)
        self.note_box = ScrolledText(self, font=('AngsanaUPC', 14), width=65,
                                     relief=FLAT, bg='white', height=9)
        self.note_box.place(x=20, y=185)

        #Check list
        self.check = Checkbutton(self, text='Favorite', bg='#FEFF92',
                      variable=self.var, activebackground='#FEFF92',
                      width=55, justify='left')
        self.check.place(x=20, y=423)
        
        #Button#
        self.add_note = Button(self, width=45, text="Add Note", 
                               bg='green', relief=FLAT, font=('Arial', 11, 'bold')
                               , command=self.create_note, fg='white',
                               activeforeground='green')
        self.add_note.place(x=20, y=457)
        self.find_note = Button(self.header, image=self.find_b, relief=FLAT, 
                              bg='gray', font=('Arial', 13, 'bold')
                                , command=self.find_notes, width=68, height=59,
                                overrelief=RIDGE, activebackground='#1E90FF')
        self.find_note.place(x=376, y=0)
        self.all = Button(self, width=31, height=2, fg='white', 
                                text="Note Storage", bg='#009cff',
                                relief=FLAT, activeforeground='#009cff', 
                                font=('Arial', 16, 'bold'),
                          command=self.note_storage)
        self.all.place(x=20, y=500)

        #Footer#
        self.last = Frame(self, bg='#1E90FF', width=450, height=25)
        self.last.place(x=0, y=575)
        self.fac = Label(self.last, fg='white', bg='#1E90FF', 
                         text="Faculty of Information Technology, KMITL")
        self.fac.place(x=110, y=3)
        self.about = Button(self.last, bg='#1E90FF', text='?', fg='white',
                            activeforeground='white', activebackground='#1E90FF'
                            , command=self.credit, relief=FLAT, width=2,
                            overrelief=RIDGE)
        self.about.place(x=426, y=0)

        
if __name__ == "__main__":
    app = MainApp()
    app.resizable(width = False, height = False)
    app.title("Note That")
    app.geometry("450x600+450+90")
    app.mainloop()
    

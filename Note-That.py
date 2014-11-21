# -*- coding: utf-8 -*-
from Tkinter import *
from ScrolledText import ScrolledText
from sqlite3 import *
import datetime

class NoteStorage(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, * args, **kwargs)

    def all_note(self):
        self.title_file = Label(self, text='All note')
        self.title_file.grid(row=0, column=0)

class Findpage(Tk):
    """
    Represent a Find page
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.find_box()

    def find_box(self):
        self.box = Entry(self, width=38, font=('AngsanaUPC', 18))
        self.box.grid(row=0, column=1)
        self.label = Label(self, text='Find', font=('AngsanaUPC', 18))
        self.label.grid(row=0, column=0)
        self.b_find = Button(self, text='search', bg='green', relief=FLAT)
        self.b_find.grid(row=1, column=1)

class Notepage(Tk):

    def __init__(self, text, *args, **kwargs):
        Tk.__init__(self, text, *args, **kwargs)
        self.text = text

    def note_pages(self, note_page):
        """
        Display a Note when add new note or edit note
        """
        #self.decorate = Frame(self, bg='red', width=400, height=35)
        #self.decorate.grid(row=0, column=0)
        self.text_main = Label(self, text=self.text, justify=LEFT,
                               font=('AngsanaUPC', 18), padx=10, pady=10,
                               bg='gray')
        self.text_main.grid(row=1, column=1)
        self.quit = Button(self, text="OK", command=note_page.quit)
        self.quit.grid(row=2, column=2)
        
class MainApp(Tk):
    """
    Represent a main page
    """

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.find_b = PhotoImage(file="Find_button.gif")
        self.window()

    def note_storage(self):

        note_store = NoteStorage()
        note_store.geometry('450x600+450+90')
        note_store.title('Note Storage')
        note_store.resizable(width=False, height=False)
        note_store.all_note()
        note_store.mainloop()

    def create_note(self):

        title_name = self.title_box.get()
        note_text = self.note_box.get('1.0', END).encode('utf-8')
        if title_name != '' and note_text != '':
            self.title_box.delete(0, END)
            self.note_box.delete('1.0', END)
            note_page = Notepage(note_text)
            note_page.geometry('400x400+450+90')
            note_page.title('New note' + ' ' + ':' + ' ' + title_name)
            note_page.note_pages(note_page)
            note_page.mainloop()
            note_page.destroy()

    def find_notes(self):

        find = Findpage()
        find.geometry('400x50+400+400')
        #find.resizable(width=False, height=False)
        find.title('Find your note')
        find.mainloop()

    def window(self):
        """
        Display Main window
        """
        #Header#
        self.header = Frame(self, width=450, height=65, bg='#1E90FF')
        self.header.place(x=0, y=0)
        title = Label(self.header, text="NoteThat", font=('MV Boli', 25, 'bold')
                           , bg='#1E90FF', fg='white')
        title.place(x=15, y=5)

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
        
        #Button#
        self.add_note = Button(self, width=12, height=1, text="Add Note", 
                               bg='green', relief=FLAT, font=('Arial', 13, 'bold')
                               , command=self.create_note, fg='white',
                               activeforeground='green')
        self.add_note.place(x=20, y=440)
        self.add_tag = Button(self, width=12, height=1, text="Add Tags",
                              bg='gray', relief=FLAT, font=('Arial', 13, 'bold'))
        self.add_tag.place(x=162, y=440)
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
        self.all.place(x=20, y=490)

        #Footer#
        self.last = Frame(self, bg='#1E90FF', width=450, height=25)
        self.last.place(x=0, y=575)
        self.fac = Label(self.last, fg='white', bg='#1E90FF', 
                         text="Faculty of Information Technology, KMITL")
        self.fac.place(x=110, y=3)

        
if __name__ == "__main__":
    app = MainApp()
    app.resizable(width = False, height = False)
    app.title("Note That")
    app.geometry("450x600+450+90")
    app.mainloop()
    

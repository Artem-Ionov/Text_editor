import sys
from tkinter import *
from GUI_MIX import *
from tkinter.messagebox import askyesno, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename

class SimpleEditor3(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.target=None
        self.MenuBar()
        self.ToolBar()
        self.Middle()

    def MenuBar(self):
        self.template=[('File', [('New', 'disable'),
                                 ('Open', self.Open),
                                 ('Save', self.Save),
                                 ('Save as', self.Save_as),
                                 ('Quit', self.Quit)]),
                       ('Edit',
                                [('Undo', self.Undo),
                                 ('Redo', self.Redo),
                                 'separator',
                                 ('Copy', self.Copy),
                                 ('Cut', self.Cut),
                                 ('Paste', self.Paste),
                                 'separator',
                                 ('Select all', self.Select_all),
                                 ('Delete', self.Delete)]),
                       ('Tools',
                                [('Settings', self.Settings),
                                 ('Find', 'disable'),
                                 ('Help', self.Help)])]
        
        top=Menu(self.master)
        self.master.config(menu=top)
        for (name, items) in self.template:
            point=Menu(top, tearoff=False)
            top.add_cascade(label=name, menu=point)
            for (offset, item) in enumerate(items):
                if item == 'separator':
                    point.add_separator()
                elif item[1]=='disable':
                    point.add_command(label=item[0], command=item[1])
                    point.entryconfig(offset, state=DISABLED)
                else:
                    point.add_command(label=item[0], command=item[1])

    def ToolBar(self):
        frm=Frame(self)
        frm.pack(side=BOTTOM, fill=X)
        
        button2(frm, 'OpenMin.png', self.Open)
        button2(frm, 'SaveMin.png', self.Save)
        button2(frm, 'CopyMin.png', self.Copy)
        button2(frm, 'PasteMin.png', self.Paste)
        button2(frm, 'ArrowLeftMin.png', self.Undo)
        button2(frm, 'ArrowRightMin.png', self.Redo)
        button2(frm, 'SettingsMin.png', self.Settings)
        button2(frm, 'QuitMin.png', self.Quit, side=RIGHT)
        
        entry=Entry(frm)
        entry.pack(side=RIGHT)
        entry.bind('<Return>', self.Find)
        entry.insert(0, 'Find...')
        self.entry=entry
        
    def Open(self):
        filename=askopenfilename(initialdir='C:\Program Files\Python311')
        if filename:
            self.text.delete('1.0', END)
            self.text.insert('1.0', open(filename).read())

    def Save(self):
        try:
            open(self.filename, 'w').write(self.text.get('1.0', END))
            self.text.edit_modified(0)
        except:
            self.Save_as()

    def Save_as(self):
        filename=asksaveasfilename(initialdir='C:\Program Files\Python311')
        if filename:            
            open(filename, 'w').write(self.text.get('1.0', END))
            self.filename=filename
            self.text.edit_modified(0)

    def Quit(self):
        if self.text.edit_modified():
            if not askyesno('Confirmation', 'Do you want to save changes?'):
                self.quit()
        else:
            self.quit()

    def Undo(self):
        try:
            self.text.edit_undo()
        except TclError:
            pass

    def Redo(self):
        try:
            self.text.edit_redo()
        except TclError:
            pass

    def Copy(self):
        try:
            text=self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except TclError:
            pass

    def Cut(self):
        try:
            text=self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
            self.text.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def Paste(self):
        try:
            text=self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

    def Select_all(self):
        self.text.tag_add(SEL, '1.0', END)

    def Delete(self):
        try:
            self.text.delete(SEL_FIRST, SEL_LAST)
        except TclError:
            pass

    def Settings(self):
        win=Toplevel()
        win.title('Settings')
        win.geometry('180x110+100+200')
        L=['Font size', 'Font style', 'Font color', 'Background']
        Start=[14, 'normal', 'black', 'white']
        Var=[]
        for i in range(0,4):
            Label(win, text=L[i], width=10).grid(row=i, column=0)
            var=StringVar()
            ent=Entry(win, textvariable=var, width=15).grid(row=i, column=1)
            var.set(Start[i])
            Var.append(var)
        self.Var=Var
        Button(win, text='Apply', command=(lambda: self.Apply())).grid(row=4, columnspan=2)

    def Apply(self):
        self.text.config(font=('times', self.Var[0].get(), self.Var[1].get()))
        self.text.config(fg=self.Var[2].get(), bg=self.Var[3].get())
        self.text.focus()

    def Find(self, event):
        target=self.entry.get()
        if target==self.target:
            start=self.text.search(target, INSERT, END)
        else:
            start=self.text.search(target, '1.0', END)
        self.target=target
        
        if start:
            stop=start+('+%dc' % len(target))
            self.text.tag_remove(SEL, '1.0', END)
            self.text.tag_add(SEL, start, stop)
            self.text.mark_set(INSERT, stop)
            self.text.see(INSERT)
            self.text.focus()
        else:
            self.text.tag_remove(SEL, '1.0', END)
            self.text.mark_set(INSERT, '1.0')
            self.text.focus()

    def Help(self):
        win=Toplevel()
        win.geometry('200x100+300+300')
        win.title('Help')
        Label(win, text='Это только начало').pack(expand=YES)
        button(win, 'OK', win.destroy, BOTTOM)
            
    def Middle(self):
        sbary=Scrollbar(self)
        sbarx=Scrollbar(self, orient='horizontal')
        text=Text(self, wrap='none', undo=1)
        sbary.pack(side=RIGHT, fill=Y)
        sbarx.pack(side=BOTTOM, fill=X)
        text.pack(side=TOP, expand=YES, fill=BOTH)
        text.config(yscrollcommand=sbary.set)
        text.config(xscrollcommand=sbarx.set)
        sbary.config(command=text.yview)
        sbarx.config(command=text.xview)
        text.focus()
        text.config(font=('times', 14))
        self.text=text

if __name__=='__main__':
    root=Tk()
    root.title('MyTextEditor')
    root.geometry('700x500+300+100')
    root.iconbitmap('PictureMin/TextEditor.ico')
    SimpleEditor3(parent=root)
    root.mainloop()

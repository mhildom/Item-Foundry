from tkinter import *
from tkinter import scrolledtext, messagebox, filedialog
import os
import sys
import json

class Item():
    def __init__(self, name, description):
        self._name = name
        self._description = description

    def updateName(self, name):
        self._name = name

    def updateDescription(self, description):
        self._description = description

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getInfo(self):
        return(self.getName(), self.getDescription())

class MainWindow():

    def __init__(self, master):
        self.loaded_items = []
        self.searched_items = []
        self.selected_item = None
        self.new_inc = 0
        self.filter_by_search = False
        self.openProject = None
        self.configPath = "Config Files/config.txt"
        self.fileChangedSinceLastSave = False

        self.master = master
        self.master.title("Item Foundry")
        self.loadConfig()
        self.initUI()

    def newItem(self,evt=''):
        for item in self.loaded_items:
            if (item.getName() == 'New Item {0}'.format(self.new_inc)):
                MsgBox = messagebox.showwarning("Item Already Exists","An item with that name already exists!")
                self.new_inc += 1
                return

        self.fileChangedSinceLastSave = True
        n = Item('New Item {0}'.format(self.new_inc),'')
        self.new_inc += 1
        self.item_list_listbox.insert(END, n.getName())
        self.loaded_items.append(n)
        self.selected_item = n
        self.item_list_listbox.selection_clear(0,END)
        for i, listbox_entry in enumerate(self.item_list_listbox.get(0,END)):
            if listbox_entry == self.selected_item.getName():
                self.item_list_listbox.selection_set(i)
                self.item_list_listbox.see(i)
                break
        self.item_editor_name_entry.delete(0,END)
        self.item_editor_description_scrolledtext.delete(1.0,END)
        self.item_editor_name_entry.insert(0,n.getName())
        self.search()

    def updateEditor(self):
        self.item_editor_name_entry.delete(0,END)
        self.item_editor_description_scrolledtext.delete(1.0,END)
        self.item_editor_name_entry.insert(0, self.selected_item.getName())
        self.item_editor_description_scrolledtext.insert(1.0, self.selected_item.getDescription())

    def getSelected(self, evt=''):
        for i in self.loaded_items:
            if i.getName() == self.item_list_listbox.get(self.item_list_listbox.curselection()):
                self.selected_item = i
                print(self.selected_item.getInfo())
                self.updateEditor()

    def reloadListbox(self):
        self.item_list_listbox.delete(0,END)
        if (self.filter_by_search):
            for item in self.searched_items:
                self.item_list_listbox.insert(END, item.getName())
        else:
            for item in self.loaded_items:
                self.item_list_listbox.insert(END, item.getName())

    def search(self):
        self.searched_items=[]
        search = self.item_list_search_box.get()

        for item in self.loaded_items:
            if search in item.getName():
                self.searched_items.append(item)
            if search in item.getDescription():
                self.searched_items.append(item)

        if (search == ''):
            self.filter_by_search = False
        else:
            self.filter_by_search = True

        self.reloadListbox()

    def deleteItem(self, evt=''):
        for i in self.item_list_listbox.curselection():
            entryname = self.item_list_listbox.get(i)
            print(entryname)
            #remove it from the visible listbox
            self.item_list_listbox.delete(i)
            #remove it from the list itself
            for item in self.loaded_items:
                if (item.getName() == entryname):
                    self.loaded_items.remove(item)
            print(self.loaded_items)

    def saveItem(self):
        for item in self.loaded_items:
            if (item.getName() == self.item_editor_name_entry.get() and item.getName() != self.selected_item.getName()):
                MsgBox = messagebox.showwarning("Item Already Exists","An item with that name already exists!")
                return

        self.fileChangedSinceLastSave = True
        for item in self.loaded_items:
            if item.getName() == self.selected_item.getName():
                item.updateName(self.item_editor_name_entry.get())
                item.updateDescription(self.item_editor_description_scrolledtext.get(1.0,'end-1c'))
                self.selected_item = item
                self.search()
                self.item_list_listbox.selection_clear(0,END)
                for i, listbox_entry in enumerate(self.item_list_listbox.get(0,END)):
                    if listbox_entry == item.getName():
                        self.item_list_listbox.selection_set(i)
                        self.item_list_listbox.see(i)
                        break

    def loadProject(self, evt='', file_path=''):
        print('Load Project: {0}'.format(file_path))
        if (file_path != None and file_path != ''):
            try:
                with open(file_path) as file:
                    self.loaded_items = []
                    self.selected_item = None
                    self.item_editor_name_entry.delete(0,END)
                    self.item_editor_description_scrolledtext.delete(1.0, END)
                    self.openProject = file_path
                    data = json.load(file)
                    self.new_inc = data['inc']
                    for item in data['item']:
                        new_item = Item(item['name'], item['description'])
                        self.loaded_items.append(new_item)
                        self.item_list_listbox.insert(END, new_item.getName())
                    self.search()
                    self.fileChangedSinceLastSave = False
                    self.project_viewer_display.config(text=file_path)
                    self.item_list_listbox.selection_set(0)
                    for i in self.loaded_items:
                        if i.getName() == self.item_list_listbox.get(0):
                            self.selected_item = i
                            self.updateEditor()
                            break

            except FileNotFoundError:
                self.loadProjectGUI()
        else:
            self.loadProjectGUI()

    def loadProjectGUI(self, evt=''):
        file_path = filedialog.askopenfilename(initialdir=os.path.dirname(sys.argv[0]))
        if (file_path != None and file_path != ''):
            self.loadProject('',file_path)

    def saveProject(self,evt='',file_path=''):
        print('Save Project: {0}'.format(self.openProject))
        data = {}
        data['inc'] = self.new_inc
        data['item'] = []
        for item in self.loaded_items:
            data['item'].append({
                'name':item.getName(),
                'description':item.getDescription()
            })
        if (file_path != None and file_path != '' and file_path != 'None'):
            self.openProject = file_path
            with open(file_path,'w') as file:
                file.write(json.dumps(data, indent=4))
            self.fileChangedSinceLastSave = False
            self.project_viewer_display.config(text=file_path)
        else:
            print('No currently open project, open the file save GUI')
            self.saveProjectGUI()

    def saveProjectGUI(self, evt=''):
        file_path = filedialog.asksaveasfile(initialfile='save', filetypes=[("JSON",".json")], defaultextension=".json").name
        if(file_path != None and file_path != ''):
            self.saveProject('',file_path)

    def newProject(self, evt=''):
        self.openProject = None
        self.loaded_items = []
        self.new_inc = 0
        self.item_list_search_box.delete(0,END)
        self.item_editor_name_entry.delete(0,END)
        self.item_editor_description_scrolledtext.delete(1.0,END)
        self.fileChangedSinceLastSave = False
        self.project_viewer_display.config(text="Unsaved New Project")

    def saveConfig(self):
        with open(self.configPath, 'w') as file:
            print("Writing openProject")
            file.write('openProject,{0}\n'.format(self.openProject))

    def loadConfig(self):
        try:
            with open(self.configPath, 'r') as file:
                for line in file:
                    line = line.split(',')
                    if (line[0] == 'openProject'):
                        self.openProject = line[1][:-1]
                        print(self.openProject)
        except FileNotFoundError:
            print('File doesnt exist')

    #When called, checks the fileChangedSinceLastSave flag to see if it needs to ask to save first, and will handle all cases. If no changes need to be saved, will prompt user if they want to quit
    #This is called from menu, keybind, and is also assigned to the windows close protocol for when the X button is pressed
    def quit(self):
        if (self.fileChangedSinceLastSave):
            MsgBox = messagebox.askyesnocancel("Unsaved Changes","Do you want to save changes before exiting?")
            if (MsgBox == True):
                self.saveProject('',self.openProject)
                self.saveConfig()
                self.master.destroy()
            elif (MsgBox == False):
                self.saveConfig()
                self.master.destroy()
            else:
                return
        else:
            if (messagebox.askquestion("Quit","Are you sure you would like to quit?") == "yes"):
                self.saveConfig()
                self.master.destroy()

    def initUI(self):
        self.pane = PanedWindow(self.master)
        self.pane.pack(fill=BOTH,expand=True,side=TOP)

        self.item_list = Frame(self.pane)
        self.item_list.config(bg='black')
        self.pane.add(self.item_list)

        self.item_editor = Frame(self.pane)
        self.item_editor.config(bg='blue')
        self.pane.add(self.item_editor)

        self.project_viewer = Frame(self.master)
        self.project_viewer.config(bg = 'yellow')
        self.project_viewer.pack(side=BOTTOM, fill=X)

        self.project_viewer_label = Label(self.project_viewer, text='Active Project: ', anchor='w')
        self.project_viewer_label.pack(side=LEFT)
        self.project_viewer_display = Label(self.project_viewer, text='No Active Project', anchor='w')
        self.project_viewer_display.pack(side=RIGHT,fill=X,expand=True)


        self.item_list_new = Button(self.item_list, text="New Item", command=self.newItem)
        self.item_list_new.pack(side=BOTTOM, fill=X)

        self.item_list_search = Frame(self.item_list)
        self.item_list_search.pack(fill=X, side=TOP)

        self.item_list_search_box = Entry(self.item_list_search)
        self.item_list_search_box.pack(side=LEFT, fill=X, expand=True)

        self.item_list_search_submit = Button(self.item_list_search, text="Search", command=self.search)
        self.item_list_search_submit.pack(side=RIGHT, fill=X)

        #Lets build our scrollbar, set it to the left of the pane we created earlier and make it expand to fill the entire height of the pane
        self.item_list_scrollbar = Scrollbar(self.item_list)
        self.item_list_scrollbar.pack(fill=Y,side=LEFT)

        #Build our custom listbox, set it to "Extended" so you can select multiple objects, and set the scrollbar to the one we just made
        self.item_list_listbox = Listbox(self.item_list, selectmode=EXTENDED, yscrollcommand=self.item_list_scrollbar.set)
        #make it take up the rest of the pane
        self.item_list_listbox.pack(fill=BOTH,side=LEFT,expand=True)
        #Lets also bind a function to the left mouse double click (AKA when we want to select an object)
        self.item_list_listbox.bind("<Double-Button-1>",self.getSelected)

        #Make a sub frame to store the item name field
        self.item_editor_name = Frame(self.item_editor)
        self.item_editor_name.pack(side=TOP,fill=BOTH)
        self.item_editor_name_label = Label(self.item_editor_name, text="Item Name:")
        self.item_editor_name_label.pack(side=LEFT)
        self.item_editor_name_entry = Entry(self.item_editor_name)
        self.item_editor_name_entry.pack(side=LEFT, fill=X, padx=5, expand=True)

        #Make a sub frame to store the item description field
        self.item_editor_description = Frame(self.item_editor)
        self.item_editor_description.pack(fill=BOTH, expand=True)
        self.item_editor_description_label = Label(self.item_editor_description, text='Item Description: ')
        self.item_editor_description_label.pack(side=TOP)
        self.item_editor_description_scrolledtext = scrolledtext.ScrolledText(self.item_editor_description)
        self.item_editor_description_scrolledtext.config(wrap=WORD)
        self.item_editor_description_scrolledtext.pack(side=TOP,fill=BOTH, expand=True)

        self.item_editor_buttons = Frame(self.item_editor)
        self.item_editor_buttons.pack(side=BOTTOM, fill=BOTH)

        self.item_editor_buttons_save = Button(self.item_editor_buttons, text='Save', command=self.saveItem)
        self.item_editor_buttons_save.pack(side=LEFT, fill=X, expand=True)

        self.menu_bar = Menu(self.master)
        self.file_menu = Menu(self.menu_bar, tearoff=0)

        self.file_menu.add_command(label="New Item", command= lambda: self.newItem(), accelerator="Ctrl+N")
        self.file_menu.add_command(label="New Project", command= lambda: self.newProject(), accelerator="Ctrl+Shift+N")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save Project", command= lambda e='': self.saveProject(e,self.openProject), accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command= lambda: self.saveProjectGUI(), accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Load Recent Project", command= lambda: self.loadProject(self.openProject), accelerator="Ctrl+Shift+O")
        self.file_menu.add_command(label="Load Project", command= lambda: self.loadProjectGUI(), accelerator="Ctrl+O")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command= self.quit, accelerator="Ctrl+Q")
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.master.bind_all("<Control-n>", self.newItem)
        self.master.bind_all("<Control-Shift-N>", self.newProject)
        self.master.bind_all("<Control-s>", lambda e='': self.saveProject(e,self.openProject))
        self.master.bind_all("<Control-Shift-S>", self.saveProjectGUI)
        self.master.bind_all("<Control-Shift-O>", lambda e='': self.loadProject(e,self.openProject))
        self.master.bind_all("<Control-o>", self.loadProjectGUI)
        self.master.bind_all("<Delete>", self.deleteItem)
        self.master.bind_all("<Control-q>", self.quit)
        self.master.config(menu=self.menu_bar)

def main():
    os.chdir(os.path.dirname(sys.argv[0]))
    root = Tk()
    foundry = MainWindow(root)
    def on_quit():
        foundry.quit()
    root.protocol("WM_DELETE_WINDOW", on_quit)
    root.mainloop()

if __name__ == "__main__":
    main()

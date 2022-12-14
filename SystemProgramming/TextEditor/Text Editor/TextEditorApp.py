from cgitb import text
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QPlainTextEdit, QStatusBar, QToolBar, QVBoxLayout, QAction, QFileDialog, QMessageBox

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence
from PyQt5.QtPrintSupport import QPrintDialog

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Text Editor')
        self.setWindowIcon(QIcon('./icons/texteditor.ico'))        
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width *2, self.screen_height *2)
        
        self.filterTypes = 'Text Documents (*.txt);; Python(*.py);; Markdown(*.md)'
        self.path = None
        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(12)
        
        mainLayout = QVBoxLayout()
        
        #editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixedFont)
        mainLayout.addWidget(self.editor)
        
        #status_bar
        self.statusBar = self.statusBar()
        
        #app_container
        containers = QWidget()
        containers.setLayout(mainLayout)  
        self.setCentralWidget(containers)
        
        #--------------------------------
        #File Menus
        #--------------------------------
        
        file_menu = self.menuBar().addMenu('&File')
        
        #--------------------------------
        #File ToolBar
        #--------------------------------
        file_toolbar = QToolBar('File')
        file_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)
        
        
        #open, save , saveAs
        
        #open
        open_file_action = QAction(QIcon('./icons/openfile.ico'), 'Open File...', self)
        open_file_action.setStatusTip('Open File')
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.file_open) 
        
        #save
        save_file_action = self.create_action(self, './icons/savefile.ico', 'Save File', 'Save File', self.file_save)
        save_file_action.setShortcut(QKeySequence.Save)
        
        save_fileAs_action = self.create_action(self, './icons/savefileas.ico', 'Save File As', 'Save File As', self.file_saveAs)
        save_fileAs_action.setShortcut(QKeySequence('Ctrl+Shift+S'))        
    
        file_menu.addActions([open_file_action, save_file_action, save_fileAs_action])
        file_toolbar.addActions([open_file_action, save_file_action, save_fileAs_action])
        
        #print_action
        print_action = self.create_action(self, './icons/print.ico', 'Print File', 'Print File', self.print_file)
        print_action.setShortcut(QKeySequence.Print)
        file_menu.addActions([print_action])
        file_toolbar.addActions([print_action])

        #--------------------------------
        #Edit Menu
        #--------------------------------
        edit_menu = self.menuBar().addMenu('&Edit')
        
        #--------------------------------
        #Edit ToolBar
        #--------------------------------
        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)
        
        #Undo, Redo Actions
        undo_action = self.create_action(self, './icons/undo.ico', 'Undo', 'Undo', self.editor.undo)
        undo_action.setShortcut(QKeySequence.Undo)
        
        redo_action = self.create_action(self, './icons/redo.ico', 'Redo', 'Redo', self.editor.redo)
        redo_action.setShortcut(QKeySequence.Redo)
        
        edit_menu.addActions([undo_action, redo_action])
        edit_toolbar.addActions([undo_action, redo_action])
        
        #clear actions
        clear_action = self.create_action(self, './icons/clear.ico', 'Clear', 'Clear', self.clear_contents)
        edit_menu.addAction(clear_action) 
        edit_toolbar.addAction(clear_action) 

        #addSeparator
        edit_menu.addSeparator()
        edit_toolbar.addSeparator()
        
        #cut, copy, paste,
        cut_action = self.create_action(self, './icons/cut.ico', 'Cut', 'Cut', self.editor.cut)
        copy_action = self.create_action(self, './icons/copy.ico', 'Copy', 'Copy', self.editor.copy)
        paste_action = self.create_action(self, './icons/paste.ico', 'Paste', 'Paste', self.editor.paste)
        select_all_action = self.create_action(self, './icons/selectall.ico', 'Select All', 'Select All', self.editor.selectAll)
        
        cut_action.setShortcut(QKeySequence.Cut)
        copy_action.setShortcut(QKeySequence.Copy)
        paste_action.setShortcut(QKeySequence.Paste)
        select_all_action.setShortcut(QKeySequence.SelectAll)
        
        edit_menu.addActions([cut_action, copy_action, paste_action, select_all_action])
        edit_toolbar.addActions([cut_action, copy_action, paste_action, select_all_action])
        
        #addSeparator
        edit_menu.addSeparator()
        edit_toolbar.addSeparator()
        
        #wrap text
        wrap_text_action = self.create_action(self, './icons/wrap.ico', 'Wrap Text', 'Warp Text', self.toggle_wrap_text)
        wrap_text_action.setShortcut('Ctrl+Shift+W')
        edit_menu.addAction(wrap_text_action)
        edit_toolbar.addAction(wrap_text_action)
        
        self.update_title()
    
    def clear_contents(self):
        self.editor.setPlainText('')
    
    def toggle_wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode()) 
               
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(parent=self, 
                                              caption='Open File', 
                                            directory='',
                                            filter = self.filterTypes)
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()
    def file_save(self):
        if self.path is None:
            self.file_saveAs()
            
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, 'w') as f:
                    f.write(text)
                    f.close()
                    
            except Exception as e:
                self.dialog_message(str(e))
        
    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
                                self,
                                'Save File As',
                                '',
                                self.filterTypes
        )
        
        text = self.editor.toPlainText()
        
        if not path:
            return
        else:
            try:
                with open(path, 'w') as f:
                    f.write(text)
                    f.close()
                
            except Exception as e:
                self.dialog_message(str(e))
                
            else:
                self.path = path
                self.update_title()
    def print_file(self):
        printDialog = QPrintDialog()
        if printDialog.exec_():
            self.editor.print_(printDialog.printer())
                          
    def update_title(self):
        self.setWindowTitle('{0} - TextEditorX'.format(os.path.basename(self.path) if self.path else 'Untitled'))
        
    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()
            

    def create_action(self,parent, icon_path, action_name, set_status_tip, triggered_method) :
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action
        
              
      
        
app = QApplication(sys.argv)
TextEditor = TextEditor()
TextEditor.show()

sys.exit(app.exec_())    
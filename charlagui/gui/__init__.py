import PySimpleGUIQt as g
from charlagui import Parser
import os, threading, logging, subprocess
from glob import iglob
import ntpath
import psutil

g.SetOptions(text_color='#545454', background_color='#f0f0f0', text_element_background_color='#f0f0f0', input_elements_background_color='#dbdbdb',
             input_text_color='#545454', text_justification='left', auto_size_buttons=True, border_width=2, button_color=('#f0f0f0', '#545454'))

class Runner:
    def __init__(self):
        self.running = False
        self.proc = None

    def runCharlatano(self):
        path = None
        for file in iglob('**/*.jar'):
            path = os.path.realpath(file)
        if path:
            batch_file = """\
        @echo off
        cd /d "%~dp0"
        title $name
        java -Xmx512m -Xms512m -jar "{}"
        pause""".format(path)
            with open(os.getcwd() + '/start.bat', 'w') as ofile:
                ofile.write(batch_file)
                ofile.close()
            self.proc = subprocess.Popen([os.getcwd() + '/start.bat'], shell=False)
            self.running = True
        else:
            g.Window('Failure', no_titlebar=True, keep_on_top=True, auto_close=True, auto_close_duration=2, layout=[
                    [g.T('Couldn\'t Find Charlatano.jar... Exiting.')]
                ]).Read()
            exit()
        self.running = True
        self.proc = None

    def killCharlatano(self):
        if self.proc and self.running:
            parent = psutil.Process(pid=self.proc.pid)
            parent.kill()
            parent.wait(5)
            self.proc = None
            self.running = False
            os.remove('start.bat')
            time.sleep(2)
        else:
            self.proc = None
            self.running = False

    def restartCharlatano(self):
        if self.proc and self.running:
            self.killCharlatano()
        self.runCharlatano()

class GUI:
    def __init__(self):
        self.parser = Parser()
        self.parser.parse_2_dict()
    def load_menu(self):
        directories = []
        for root, dirs, files in os.walk("."):
            for dir in dirs:
                directories.append(dir)
        if 'settings' not in directories:
            g.Window('Error', no_titlebar=True, keep_on_top=True, auto_close=True, auto_close_duration=3, layout=[
                [g.T('Error, Missing Settings Folder. Are you in the Charlatano Build Folder?')]
            ]).Read()
            exit()
        else:
            g.Window('Success', no_titlebar=True, keep_on_top=True, auto_close=True, auto_close_duration=2, layout=[
                [g.T('Loading Settings...')]
            ]).Read()
            self.first_menu()
        
    def first_menu(self):
        layout = [
            [g.T('Charlatano GUI Settings v1.1', font=('Arial', 15))],
            [g.T('Made by Max Bridgland', font=('Arial', 10))]
        ]
        count = 0
        col1 = []
        col2 = []
        for k, v in self.parser.current_settings.items():
            title = str(k[0].upper() + k[1:].lower().replace('_', ' '))
            if (count % 2) == 0:
                col1.append([
                    g.B(' ' + title + ' ', key=k)
                ])
                count += 1
            else:
                col2.append([
                    g.B(' ' + title + ' ', key=k)
                ])
                count += 1
        layout.append([
            g.Column(col1), g.Column(col2)
        ])
        layout.append([
            g.Button('Close'), g.Button('Restart Charlatano', key='__RESTART__'), g.Button('Start Charlatano', key='__START__')
        ])
        window = g.Window('Charlatano GUI Settings', no_titlebar=True, grab_anywhere=True, keep_on_top=True, layout=layout)
        charla = Runner()
        while True:
            event, values = window.Read()
            print(event)
            if event == 'Close':
                window.Close()
                exit()
            elif event == '__START__':
                if charla.running and charla.proc:
                    charla.killCharlatano()
                    window.FindElement('__START__').Update('Start Charlatano')
                else:
                    charla.runCharlatano()
                    window.FindElement('__START__').Update('Stop Charlatano')
            elif event == '__RESTART__':
                charla.restartCharlatano()
                if charla.running:
                    window.FindElement('__START__').Update('Stop Charlatano')
            else:
                window.Close()
                self.settings_gui(event)
                
    def settings_gui(self, setting):
        layout = [
            [g.T(setting[0].upper() + setting[1:], font=('Arial', 15))]
        ]
        count = 0
        col1 = []
        col2 = []
        col3 = []
        col4 = []
        for k, v in self.parser.current_settings[setting].items():
            if count == 0:
                col1.append([
                    g.T(str(k[0].upper() + k[1:].lower().replace('_', ' '))), g.Input(str(v.replace('\n', '')), key=k)
                ])
                count += 1
            elif count == 1:
                col2.append([
                    g.T(str(k[0].upper() + k[1:].lower().replace('_', ' '))), g.Input(str(v.replace('\n', '')), key=k)
                ])
                count += 1
            elif count == 2:
                col3.append([
                    g.T(str(k[0].upper() + k[1:].lower().replace('_', ' '))), g.Input(str(v.replace('\n', '')), key=k)
                ])
                count = 0
        layout.append([
            g.Column(col1), g.Column(col2), g.Column(col3)
        ])
        layout.append([
            g.Button('Back'), g.B('Save')
        ])
        window = g.Window(setting[0].upper() + setting[1:], no_titlebar=True, grab_anywhere=True, keep_on_top=True, layout=layout)
        while True:
            event, values = window.Read()
            if event == 'Back':
                window.Close()
                self.first_menu()
            if event == 'Save':
                self.parser.update_settings(setting, values)

# runCharlatano()
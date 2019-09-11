import PySimpleGUIQt as g
from charlagui import Parser
import os

g.SetOptions(text_color='#545454', background_color='#f0f0f0', text_element_background_color='#f0f0f0', input_elements_background_color='#dbdbdb',
             input_text_color='#545454', text_justification='left', auto_size_buttons=True, border_width=2, button_color=('#f0f0f0', '#545454'))

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
            [g.T('Charlatano GUI Settings', font=('Arial', 15))],
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
            g.Button('Close')
        ])
        window = g.Window('Charlatano GUI Settings', no_titlebar=True, grab_anywhere=True, keep_on_top=True, layout=layout)
        while True:
            event, values = window.Read()
            if event == 'Close':
                window.Close()
                exit()
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
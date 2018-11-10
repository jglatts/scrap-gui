"""
PySimpleGui program that displays web content from beautifulsoup/requests. 
TODO:
    - text format/color/size
    - import the scrapping module
    - errors along the way
"""

#!/usr/bin/env python
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup


""" Scraps a website, needs to be displayed better though """
def drudgeGuy():
    url = ''    #enter website-url here
    source_code = requests.get(url)
    plain_text = source_code.text 
    soup = BeautifulSoup(plain_text, "html.parser") 
    if soup:
        for column in soup.find_all('a'):
            print("SCRAPING %s" % url)
            return soup.get_text()
    else:
        return
    

""" Currently not used, but easy to implement if need be """
def SecondForm():
    sg.ChangeLookAndFeel('TealMono')
    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK(button_color=('black', 'red'))]]

    window = sg.Window('Second Form').Layout(layout)
    b, v = window.Read()


def TestMenus():
    sg.ChangeLookAndFeel('GreenMono')
    sg.SetOptions(element_padding=(10, 0))

    layout = [
               [sg.PopupScrolled("JDG", drudgeGuy())],
               [sg.In('JDG', key='input', do_not_clear=False)],
               [sg.OK(button_color=('black', 'red'))]
             ]

    window = sg.Window("JDG Drude Feed", default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=False, auto_close_duration = 2).Layout(layout)
    window.Read()



TestMenus()

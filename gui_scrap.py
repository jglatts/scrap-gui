"""

Drudge Report Scrapper w/ nice GUI
The hope is to import the module that does the actual scrapping

"""
#!/usr/bin/env python
#IMPORT DRUDGE-SCRAP module
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import sys
import time
import faker
from faker import Faker


def fakeInfo():
    fake = Faker()
    names = []
    display_names = []
    
    for x in range(20):
        names.append(fake.name())
    
    for i in names:
        j = i.replace(' ',')                                                                                ')
        display_names.append(j)

    return display_names

""" Scraps drudge, needs to be displayed better though """
def drudgeGuy():
    url = 'http://drudgereport.com'
    source_code = requests.get(url) # pass the url to requests, HTTP for humans
    plain_text = source_code.text 
    soup = BeautifulSoup(plain_text, "html.parser") # pass/parse the url with bs4
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

    fkmod = Faker()

    # ------ GUI Defintion ------ #
    layout = [
               [sg.PopupScrolled("JDG", fkmod.name(), drudgeGuy())],
               [sg.In('JDG', key='input', do_not_clear=False)],
               [sg.OK(button_color=('black', 'red'))]
             ]

    window = sg.Window("JDG Drude Feed", default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=False, auto_close_duration = 2).Layout(layout)

    # ------ Start the GUI ------ #
    window.Read()




TestMenus()
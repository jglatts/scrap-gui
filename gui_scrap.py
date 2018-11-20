import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup
import string


""" Scraps a website, needs to be displayed better though """
class getSoup(object):
    def __init__(self, url):
        super(getSoup, self).__init__()
        self.url = url

        
""" add **args here to search for differnt elements """
    def scrap(self):
        user_url = self.url 
        source_code = requests.get(user_url)
        plain_text = source_code.text 
        soup = BeautifulSoup(plain_text, "html.parser") 
        if soup:
            for column in soup.find_all('a'):
                print("SCRAPING %s" % user_url)
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
    # add website-urls here 
    url_one = getSoup("https://.com/").scrap()
    url_two = getSoup("https://.com/").scrap()
    
    # helper function on the way to get rid of repetition
    output = url_one.strip()
    filtered_one = ''
    for char in output:
        if char in string.printable:
            filtered_one += char

    output_two = url_two.strip()
    filtered_two = ''
    for char_two in output_two:
        if char_two in string.printable:
            filtered_two += char_two

    sg.ChangeLookAndFeel('GreenMono')
    sg.SetOptions(element_padding=(10, 0))

    layout = [
               [sg.Multiline(filtered_one, size=(80,40)),
               sg.Multiline(filtered_two, size=(80,40))],
               [sg.In('JDG', key='input', do_not_clear=False)],
               [sg.OK(button_color=('black', 'red'))]
             ]

    window = sg.Window("JDG Drude Feed", default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=False, auto_close_duration = 2).Layout(layout)
    window.Read()

TestMenus()

"""

- Refactor Mane!!! Very cluttered at the moments

"""
import PySimpleGUI as sg
import requests
import string
from bs4 import BeautifulSoup
from faker import Faker


class GetSoup(object):
    """ Scraps a website for the GUI to display. A function call may be easier, but we out here learning OOP. """

    def __init__(self, url):
        super(GetSoup, self).__init__()
        self.url = url

    """ determine how bs4 will search the provided urls.  """
    """ Find the more effective way. """
    def scrap(self, quick_search=True):
        user_url = self.url
        source_code = requests.get(user_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        if soup:
            # logical error here, prints the wrong url
            print("SCRAPING %s" % user_url)
            # change the tags that bs4 will search for, find more effective way of doing so
            if quick_search:
                # drudge-gui, so this will have 3 columns of content
                for column in soup.find_all("td"):
                    return column.get_text()
            else:
                # not finding all elements
                for column in soup.find_all("a"):
                    return column.get_text()
        else:
            return



def begin_form():
    """ Prompt the user which site to scrap, input via buttons and text """

    sg.ChangeLookAndFeel('TealMono')
    layout = [
                [sg.Text('Scrap Feed!', size=(21, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE)],
                [sg.Button('Drudge-GUI', button_color=('black', 'red'), font=("Helvetica", 35)),
                 sg.Button('Google-GUI', font=("Helvetica", 35))]
             ]

    window = sg.Window('Whadup Mane').Layout(layout)
    while True:
        button, value = window.Read()
        if button == 'Drudge-GUI':
            test_menus()
        elif button == 'Google-GUI':
            test_menus(False)
        else:
            return


def test_menus(check=True):
    """ Display information """

    # add website-urls here
    url_one = GetSoup("https://www.drudgereport.com/").scrap()
    url_two = GetSoup("https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en").scrap(False)

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
    sg.SetOptions(element_padding=(5, 0))

    if check:
        layout = [
            [sg.Text('Drudge Report', size=(20, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                     relief=sg.RELIEF_RIDGE)],
            [sg.Multiline(filtered_one, size=(70, 12))],
            # sg.Multiline(filtered_two, size=(80, 20))],
            [sg.In('JDG', key='input', do_not_clear=True)],
            [sg.Button('HOME', button_color=('black', 'red')), sg.Button('EXIT')]
        ]

        window = sg.Window("WEAS Feed", default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=True).Layout(layout)
        # read values from buttons and respond accordingly
        while True:
            event, value = window.Read()
            if event == 'HOME':
                begin_form()
            else:
                return
    else:
        layout = [
            [sg.Text('Google-News', size=(20, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                     relief=sg.RELIEF_RIDGE)],
            #[sg.Multiline(filtered_one, size=(80, 20)),
            [sg.Multiline(filtered_two, size=(70, 12))],
            [sg.In('JDG', key='input', do_not_clear=True)],
            [sg.Button('HOME', button_color=('black', 'red')), sg.Button('EXIT')]
        ]

        window = sg.Window("WEAS Feed", default_element_size=(12, 1), auto_size_text=False,
                           auto_size_buttons=True).Layout(layout)
        # read values from buttons and respond accordingly
        while True:
            event, value = window.Read()
            if event == 'HOME':
                begin_form()
            else:
                return


begin_form()

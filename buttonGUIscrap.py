import PySimpleGUI as sg
import requests
import string
from bs4 import BeautifulSoup
from faker import Faker


class GetSoup(object):
    """ Scraps a website, needs to be displayed better though """

    def __init__(self, url):
        super(GetSoup, self).__init__()
        self.url = url

    """ add **args here to search for different elements """
    """ something like a flag that will change the bs4 scrap """
    def scrap(self, quick_search=True):
        user_url = self.url
        source_code = requests.get(user_url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        if soup:
            # logical error here, prints the wrong url
            print("SCRAPING %s" % user_url)
            if quick_search:
                for column in soup.find_all("td"):
                    print(column.get_text())
                    return column.get_text()
            else:
                for column in soup.find_all("a"):
                    print(column.get_text())
                    return column.get_text()
        else:
            return


def begin_form():
    """ Prompt the user which site to scrap, input via buttons and text """

    sg.ChangeLookAndFeel('TealMono')
    layout = [
                [sg.Text('Scrap Feed!', size=(21, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE)],
                [sg.Button('Site1-GUI', button_color=('black', 'red'), font=("Helvetica", 35)),
                 sg.Button('Site2-GUI', font=("Helvetica", 35))]
             ]

    window = sg.Window('Whadup Mane').Layout(layout)
    while True:
        button, value = window.Read()
        if button == 'Site1-GUI':
            test_menus()
        elif button == 'Site2-GUI':
            test_menus(False)
        else:
            return


def test_menus(check=True):
    """ Display information """

    # add website-urls here
    url_one = GetSoup("").scrap()
    url_two = GetSoup("").scrap(False)

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
    sg.SetOptions(element_padding=(8, 0))

    if check:
        layout = [
            [sg.Text('Web Feed!', size=(45, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                     relief=sg.RELIEF_RIDGE)],
            [sg.Multiline(filtered_one, size=(80, 40))],
            # sg.Multiline(filtered_two, size=(80, 40))],
            [sg.In('JDG', key='input', do_not_clear=True)],
            [sg.Button('HOME', button_color=('black', 'red')), sg.Button('EXIT')]
        ]

        window = sg.Window("Web Feed", default_element_size=(12, 1), auto_size_text=False, auto_size_buttons=True).Layout(layout)
        # read values from buttons and respond accordingly
        while True:
            event, value = window.Read()
            if event == 'HOME':
                begin_form()
            else:
                return
    else:
        layout = [
            [sg.Text('Web Feed!', size=(45, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                     relief=sg.RELIEF_RIDGE)],
            #[sg.Multiline(filtered_one, size=(80, 40)),
            [sg.Multiline(filtered_two, size=(80, 40))],
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

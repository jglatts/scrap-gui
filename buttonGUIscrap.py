"""

- Refactor Mane!!! Very cluttered at the moments

"""
import PySimpleGUI as sg
import requests
import string
from bs4 import BeautifulSoup
from faker import Faker


def bayscrap(products):
    """ Get some info from EBAY with requests and bs4. """
    """ Add empty scrap check """
    url = 'https://www.ebay.com/sch/' + products
    # Add headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    source_code = requests.get(url, headers=headers)  # pass the url to requests, HTTP for humans
    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, "html.parser")  # pass/parse the url with bs4
    for items in soup.find_all("div", {"class": "s-item__info clearfix"}):
        print('\n' + items.get_text())

    soldlistings(products)



def soldlistings(products):
    """ Scrap EBAY for sold items of the search product.
    This changes the url to find the sold listings.
    New URL will be fed to requests\bs4.  """

    print('\nDisplaying Sold Items For:' + ' ' + products.title() + '\n')
    sold_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + products + '&_sacat=0&LH_Sold=1&_dmd=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    src_sold = requests.get(sold_url, headers=headers)  # pass the url to requests, HTTP for humans
    bs4_text = src_sold.text

    # Throw findings to bs4 then display
    sold_soup = BeautifulSoup(bs4_text, 'html.parser')
    for sold in sold_soup.find_all("li", {"class": "s-item"}):
        print('\n' + sold.get_text())


def begin_form():
    """ Prompt the user what products to find """

    sg.ChangeLookAndFeel('TealMono')
    layout = [
                [sg.Text('Search Ebay!', size=(21, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE)],
                # change to text input field
                [sg.Text('Enter products to search for', pad=(210, 5))],
                [sg.InputText(focus=True, pad=(130, 5))],
                [sg.Button('Find Products', button_color=('black', 'red'), font=("Helvetica", 15), pad=(225, 5))]
             ]

    window = sg.Window('Find Products').Layout(layout)
    while True:
        button, value = window.Read()
        if button == 'Find Products':
            # call bayscrap() and pass the inputtext over
            val_string = ''.join(value)
            print(val_string)
            bayscrap(val_string)
        # change to check for text input
        else:
            return

"""
def test_menus(check=True):
   """ """ Display information """"""

    # add website-urls here

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

"""

begin_form()

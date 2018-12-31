#!/usr/bin/env python
#
# Author: John Glatts
# This is a program for searching\scraping EBAY.
# Search for Products, and see when\how much they sold for.
#
#
import PySimpleGUI as sg
import requests
import string
from bs4 import BeautifulSoup


def bayscrap(products):
    """ Get some info from EBAY with requests and bs4.
        Add empty scrap check
    """

    url = 'https://www.ebay.com/sch/' + products
    # Add headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text

    content = ''
    str_links = ''
    soup = BeautifulSoup(plain_text, "html.parser")
    for items in soup.find_all("div", {"class": "s-item__info clearfix"}):
        # attach links as they're found
        for links in items.find_all("a", href=True):
            # maybe overkill?
            print(links['href'])
            for link_char in links['href']:
                if link_char in string.printable:
                    str_links += link_char
            #str_links.append(links['href'])
        # check where this is going
        content += str_links
        # filtering
        for char in items.get_text():
            if char in string.printable:
                content += char
        content += '\n\n\n'

    return content


def get_sold_scrap(products):
    """ Scrap EBAY for sold items of the search product. """

    print('\nDisplaying Sold Items For:' + ' ' + products.title() + '\n')
    sold_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + products + '&_sacat=0&LH_Sold=1&_dmd=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    src_sold = requests.get(sold_url, headers=headers)
    bs4_text = src_sold.text

    sold_soup = BeautifulSoup(bs4_text, 'html.parser')
    filtered = ''
    # trying to attach links as they're found
    for sold in sold_soup.find_all("li", {"class": "s-item"}, "a"):
        # print('\n' + sold.get_text())
        for char in sold.get_text():
            if char in string.printable:
                filtered += char
        filtered += '\n\n\n'

    return filtered


def sold_form(product, number_search):
    """ GUI for sold products """

    content = get_sold_scrap(product)
    sg.ChangeLookAndFeel('GreenMono')
    heading = ("sold %s-products" % product)

    layout = [
        [sg.Text(heading.title(), size=(30, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE, pad=(235, 3))],
        [sg.Multiline(content, size=(175, 15))],
        [sg.In('JDG', key='input', do_not_clear=True)],
        [sg.Button('HOME', button_color=('black', 'white')), sg.Button('Sold-Listings',
                                                                       button_color=('black', 'white')),
         sg.Button('EXIT', button_color=('black', 'white'))]
    ]

    window = sg.Window("Ebay Feed", default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=True, border_depth=5).Layout(layout)

    # read values from buttons and respond accordingly
    while True:
        event, value = window.Read()
        if event == 'HOME':
            begin_form(searches, number_search)
        elif event == 'Sold-Listings':
            sold_form(product, number_search)
        else:
            exit_dsply(number_search)
            return


def begin_form(searches, number_search):
    """ Prompt the user what products to find """

    sg.ChangeLookAndFeel('GreenMono')
    menu_def = [
        ['Search History', ['&All Searches']],
        ['URL Info', ['&Change Site']],
        ['About', ['&All Searches', '&Help']],
    ]
    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text('Search Ebay!', size=(21, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE)],
        [sg.Text('Enter products to search for', pad=(180, 0), font=("Helvetica", 13))],
        [sg.InputText(focus=True, pad=(120, 0))],
        [sg.Button('Find Products', button_color=('black', 'red'), font=("Helvetica", 15), pad=(215, 10),
                   bind_return_key=True)]
    ]

    window = sg.Window('Find Products', border_depth=5).Layout(layout)
    while True:
        button, value = window.Read()
        if button == 'Find Products':
            number_search += 1
            val_string = ''.join(value[1])
            print(val_string)
            # keep track of the searches
            searches.append(val_string)
            print('\n%d\n' % number_search)
            product_page(val_string, number_search)
        elif button == 'All Searches':
            all_searches(searches, number_search)
        elif button == 'Change Site':
            # is there a less harsh way to window.Hide()?
            window.Hide()
            change_gui()
            window.UnHide()
        elif button == 'Help':
            # add func() call here
            pass
        else:
            # getting trash values for number_search
            exit_dsply(number_search)
            return


def product_page(product, number_search):
    """ Initial GUI product page. Scraps ebay for products.
        TODO:
            - add links
            - more button options
            - format improvements
     """

    output = bayscrap(product)
    # print(filtered)
    sg.ChangeLookAndFeel('GreenMono')
    heading = ("%s-products" % product)

    layout = [
        [sg.Text(heading.title(), size=(30, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE, pad=(235, 3))],
        [sg.Multiline(output, size=(175, 15))],
        [sg.In('JDG', key='input', do_not_clear=True)],
        [sg.Button('HOME', button_color=('black', 'white')),
         sg.Button('Sold-Listings', button_color=('black', 'white')),
         sg.Button('EXIT', button_color=('black', 'white'))]
    ]

    window = sg.Window("Ebay Feed", default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=True, border_depth=5).Layout(layout)

    # having trouble re-sizing the window
    window.Size = 190, 50

    # read values from buttons and respond accordingly
    while True:
        event, value = window.Read()
        if event == 'HOME':
            begin_form(searches, number_search)
        elif event == 'Sold-Listings':
            sold_form(product, number_search)
        # same functionality as HOME btn
        # upgrade this ish
        else:
            exit_dsply(number_search)
            return


def new_scrap(new_url):
    """ Scrap the new site and return some info """
    pass # for now


def change_gui():
    """ Change the site and find more info """
    sg.ChangeLookAndFeel('LightGreen')
    menu_def = [
        # wire new menu
        #['', ['']],
    ]
    layout = [
        # add a new menu later
        #[sg.Menu(menu_def, tearoff=True)],
        [sg.Text('New Site', size=(21, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE)],
        [sg.Text('Enter a new website (just the name)', pad=(180, 0), font=("Helvetica", 13))],
        [sg.InputText(focus=True, pad=(120, 0))],
        [sg.Button('Scrap Site', button_color=('black', 'red'), font=("Helvetica", 15), pad=(215, 10),
                   bind_return_key=True)]
    ]
    window = sg.Window('New Site', border_depth=5).Layout(layout)
    while True:
        # call the GUI with Read()
        button, value = window.Read()
        if value == 'Scrap Site':
            # UNCOMMENT TO HOOK-UP
            get_string = ''.join(value[1])
            # call helper func() and pass val_string
            #new_scrap(get_string)
            begin_form(searches, number_search)


def new_scrap(new_url):
    """ Scrap a new url that the user provides
        Don't rewrite other GUI's, wire this one to them
    """
    url = 'https://www.' + new_url + '.com'  # get new base url
    # Add headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text

    content = ''
    soup = BeautifulSoup(plain_text, "html.parser")
    output = soup.prettify()

    # get the size in order to fill format the content
    size = len(soup.prettify())
    for i in range(size):
        for char_two in output:
            if char_two in string.printable:
                content += char_two

        content += '\n'

    # call the GUI to display new sit
    display_new_site(content)


def display_new_site(output):
    """  """


def exit_dsply(no_searches):
    """ Print the number of searches made when the user exits """
    # Printing multiple lines, figure out bug
    # print("\nYou made %d searches" % no_searches)


def all_searches(search_hist, size):
    """ Print all the searches that have been made """
    if size == 1:
        sg.Popup("You've made %d search" % size)
    else:
        sg.Popup("You've made %d searches" % size)


# begin program with fresh search history
searches = []
# double check where number_search is incrementing
number_search = 0
begin_form(searches, number_search)

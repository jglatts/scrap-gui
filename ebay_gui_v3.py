#!/usr/bin/env python
#
# Author: John Glatts
# This is a program for searching\scraping EBAY.
# Search for Products, and see when\how much they sold for.
#
#
import string
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup


def display_gui(items, links):
    """ GUI to display items and links """
    sg.ChangeLookAndFeel('GreenMono')
    heading = "Ebay GUI"
    link_title = "Links"

    layout = [
        [sg.Text(heading.title(), size=(30, 1), justification='center', font=("Helvetica", 35), text_color="blue",
                 relief=sg.RELIEF_RIDGE, pad=(120, 3))],
        [sg.Multiline(items, size=(155, 12))],
        [sg.Text(link_title, text_color="blue", font=("Helvetica", 15), pad=(50, 3))],
        [sg.Multiline(links, size=(155, 12))],
        [sg.In('JDG', key='input', do_not_clear=True)],
        [sg.Button('HOME', button_color=('black', 'white')), sg.Button('Sold-Listings',
                                                                       button_color=('black', 'white')),
         sg.Button('EXIT', button_color=('black', 'white'))]
    ]

    window = sg.Window("Ebay Feed", default_element_size=(12, 1), auto_size_text=False,
                       auto_size_buttons=True, border_depth=5).Layout(layout)

    # read values from buttons and respond accordingly
    while True:
        window.Read()


def bayscrap():
    """ Get some info from EBAY with requests and bs4. """

    check_words = ['yes', 'YES', 'Yes']

    str_items = ''
    str_links = ''
    while True:
        try:
            print('\nWhat Do You Want To View From Ebay?')
            search = input()
            url = 'https://www.ebay.com/sch/' + search

            # Add headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
            source_code = requests.get(url, headers=headers)  # pass the url to requests, HTTP for humans
            plain_text = source_code.text

            # Display findings
            soup = BeautifulSoup(plain_text, "html.parser")
            for items in soup.find_all("div", {"class": "s-item__info clearfix"}):
                # Find the links
                for links in items.find_all("a", href=True):
                    pass
                print('\n' + items.get_text())
                print(links['href'])
                # Filter the content for the GUI
                for char in items.get_text():
                    if char in string.printable:
                        str_items += char
                str_items += '\n\n\n'
                for char_link in links:
                    # issue using string.printable and links
                    #if char_link in string.printable:
                    str_links += links['href']
                str_links += '\n\n\n'

            # Test call to GUI
            display_gui(str_items, str_links)

            print('\n\n View sold listings for %s?' % search.title())
            check = input()
            if check in check_words:
                soldlistings(search)
            else:
                print('\nOK!\n')
                return

        except KeyboardInterrupt:
            print('\n\n\n\tProgram Canceled\n\n\n')
            return


def soldlistings(search_item):
    """ Scrap EBAY for sold items of the search product.
    This changes the url to find the sold listings.
    New URL will be fed to requests\bs4.  """

    print('\nDisplaying Sold Items For:' + ' ' + search_item.title() + '\n')
    sold_url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=' + search_item + '&_sacat=0&LH_Sold=1&_dmd=2'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    src_sold = requests.get(sold_url, headers=headers)  # pass the url to requests, HTTP for humans
    bs4_text = src_sold.text

    # Throw findings to bs4 then display
    sold_soup = BeautifulSoup(bs4_text, 'html.parser')
    for sold in sold_soup.find_all("li", {"class": "s-item"}):
        for links in sold.find_all("a", href=True):
            pass
        print('\n' + sold.get_text())
        print(links['href'])


bayscrap()

import requests
import re
import config
from bs4 import BeautifulSoup


def parse_beer(beer_name):
    array = []
    url = "https://www.kupi.cz/hledej?f=" + beer_name + "&vse=0"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find all braniks
    product = soup.find_all('div', class_="group_discounts active")
    name_dict = {}
    for entry in product:
        # make dictionary with product tag and proper name
        title = entry.h2.find('a')["title"]
        data_product = entry.find('a')["data-product"]
        name_dict.update({data_product: title})

    shops = soup.find_all('tr', class_="only_discount")
    for shop in shops:
        # find stuff
        array_temp = {}
        store = shop.find('span', class_="discounts_shop_name").find_next().getText()
        store = " ".join(store.split())

        # Kupi.cz has an error with Tesco's name: it ends with a ' '.
        # This checks and removes the last character if it's a ' '.
        if store[-1] == " ":
            store = store[:-1]

        # Idiots at kupi.cz forget to tag volumes some times.
        try:
            size = shop.find('div', class_="discount_amount left").getText().strip().replace('\xa0', ' ')
            size = re.sub(r'[^\d.x]', '', size)
        except AttributeError:
            size = ''

        price = shop.find('strong').getText().strip().replace('\xa0', ' ')
        note = shop.find('div', class_="discount_note")
        note_pattern = re.compile('láhev|pet láhev|plech|láhve')

        if note is not None:
            note = note.getText().strip().replace('\xa0', ' ')
            try:
                note = ', ' + note_pattern.findall(note)[0]
            except IndexError:
                note = ''
        else:
            note = ''

        # change string to proper name of beer
        valid_discount = shop.find('td', class_="text-left discounts_validity valid_discount")
        if valid_discount is not None:
            for key in name_dict:
                if key == shop.find('a', class_="product_link_history")["data-product"]:
                    beer = name_dict[key]

            array_temp.update({'size': size, 'beer': beer,  'price': price, 'store': store, 'note': note})
            array.append(array_temp)

    f = open("akce/" + beer_name, "w")
    for size in config.sizes_list:
        name_counter = ''
        for dic in array:
            if name_counter != dic['beer'] and dic['size'] == size:
                name_counter = dic['beer']
                f.write(f"\n*{name_counter} / {dic['size']} l:*\n")
                f.write(f"{dic['price']} - {dic['store']}{dic['note']}\n")
            elif name_counter == dic['beer'] and dic['size'] == size:
                f.write(f"{dic['price']} - {dic['store']}{dic['note']}\n")
    f.close()

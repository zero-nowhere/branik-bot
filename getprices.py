import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.kupi.cz/hledej?f=branik&vse=0")
soup = BeautifulSoup(page.content, 'html.parser')

# Find all braniks
product = soup.find_all('div',class_="group_discounts active")
name_dict = {}
for entry in product:
	# make dictionary with product tag and proper name
	title = entry.h2.find('a')["title"]
	data_product = entry.find('a')["data-product"]
	name_dict.update({ data_product : title })

f = open("akce", "w")

array = []
shops = soup.find_all('tr',class_="only_discount")
for shop in shops:
	# find stuff
	array_temp = {}
	store = shop.find('span',class_="discounts_shop_name").find_next().find('span').getText()
	size = shop.find('div',class_="discount_amount left").getText().strip().replace('\xa0', ' ')
	price = shop.find('strong').getText().strip().replace('\xa0', ' ')
	note = shop.find('div',class_="discount_note").getText().strip().replace('\xa0', ' ')
	# change string to proper name of beer
	valid_discount = shop.find('td', class_="text-left discounts_validity valid_discount")
	if valid_discount != None:
		for key in name_dict:
			if key == shop.find('a',class_="product_link_history")["data-product"]:
				beer = name_dict[key]

		array_temp.update({"price" : price, "size" : size, "beer" : beer, "store" : store, "note" : note})
		array.append(array_temp)


name_counter = ''
for dic in array:
	if name_counter != dic['beer'] and dic['size'] == "/ 0.5 l":		
		name_counter = dic['beer']
		f.write(f"\n*{name_counter} {dic['size']} :*\n")
		f.write(f"{dic['price']} - {dic['store']}\n")
	elif name_counter == dic['beer'] and dic['size'] == "/ 0.5 l":
		f.write(f"{dic['price']} - {dic['store']}\n")


name_counter = ''
for dic in array:
	if name_counter != dic['beer'] and dic['size'] == "/ 2 l":		
		name_counter = dic['beer']
		f.write(f"\n*{name_counter} {dic['size']} :*\n")
		f.write(f"{dic['price']} - {dic['store']}\n")
	elif name_counter == dic['beer'] and dic['size'] == "/ 2 l":
		f.write(f"{dic['price']} - {dic['store']}\n")


f.close()
print('0')
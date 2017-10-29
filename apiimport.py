import json
import requests

from Functions import*


#resp = requests.get('https://world.openfoodfacts.org/language/1/.json')
#if resp.status_code != 200:
    # This means something went wrong.
#    raise ApiError('GET /produit/ {}'.format(resp.status_code))

#print (resp.json()['count']//20+1)


#for i in range(20):
#    print(resp.json()['products'][i]['brands'])



#resp = requests.get('https://world.openfoodfacts.org/country/france/1000.json')
#print (resp.json())

#c = resp.json()['products'][5] #['categories']
#print(c)
#print(c.split(','))

#aliment_test = Product()
#aliment_test.jsonread(c)

#print(aliment_test.link)
#print(aliment_test.categories)

#cat = Category()
#tst = requests.get('https://fr.openfoodfacts.org/categories.json')
#cat.load(tst.json()['tags'][18])


test = Categories()
test.overview()
#print(cat.name, cat.off_id, cat.elem_count)



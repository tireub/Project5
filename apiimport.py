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



resp = requests.get('https://world.openfoodfacts.org/country/france/300.json')
#print (resp.json())

plop = resp.json()['products'][18] #['categories']
#print(plop)
#print(c.split(','))

#aliment_test = Product()
#aliment_test.jsonread(c)

#print(aliment_test.link)
#print(aliment_test.categories)

#print(aliment_test.categories[1])
#print(index)
#cat = Category()
#tst = requests.get('https://fr.openfoodfacts.org/categories.json')
#cat.load(tst.json()['tags'][18])


test = Categories()
db = MySQLdb.connect(host="localhost",user="root",passwd="Davemurray33",db="foodfacts")
#test = Product()
#test.jsonread(plop)
#test.parenthood_fill(db)

#print(len(''))
#test.aliment_fill(db)
#c = db.cursor()
#query = ("SELECT id FROM Categories WHERE name = 'Sodas light'")
#c.execute(query)
#print(c.fetchall())
#tuple = []
#for id in c:
#    print(id)
#    tuple.append(id)
#print(tuple[0])

#test = Product()
#test.categories = ('Aliments et boissons à base de végétaux', "Aliments d'origine végétale", 'Epicerie',
#                   'Produits déshydratés', 'Bouillons', 'Produits lyophilisés à reconstituer', 'Bouillons déshydratés',
#                   'Bouillons de légumes', 'Bouillons cubes')
#test.categories = list(map(str.encode('ascii')[:39], unicodedata.normalize('NFKD', test.categories)))
#print(test.categories)


#test.name = 'alimenttest'
#test.link = 'openclassrooms.com'
#test.grade = 2
#test.parenthood_fill(db)
#test.aliment_fill(db)

#print(test.categories)
#test.parenthood_fill(db)
#print(test.finest_cat)





#test.overview(db)
#print(cat.name, cat.off_id, cat.elem_count)

fillelements(db)

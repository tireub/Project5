import json
import MySQLdb
import requests
import unicodedata

class Product:
    #product class

    #def intialisation
    def __init__(self):
        self.name = ''
        self.link = ''
        self.categories = ''
        self.ingredients = ''
        self.grade = 0
        self.brand = ''
        self.stores = ''

    #def import from json
    def jsonread(self, json_file):
        if 'product_name_fr' in json_file:
            self.name = json_file['product_name_fr']
        if 'code' in json_file:
            self.link = 'https://fr.openfoodfacts.org/produit/'+json_file['code']
        if 'categories' in json_file:
            self.categories = json_file['categories']
        if 'ingredients' in json_file:
            self.ingredients = json_file['ingredients']
        if 'nutrition_grade_fr' in json_file:
            self.grade = json_file['nutrition_grade_fr']
        if 'brands' in json_file:
            self.brand = json_file['brands']
        if 'sores' in json_file:
            self.stores = json_file['stores']
        if 'categories' in json_file:
            self.categories = json_file['categories'].split(',')

    #def insert into database
    #def database_insert(self, basename):

class Categories:

    def overview(self):
        tst = requests.get('https://fr.openfoodfacts.org/categories.json')
        max = tst.json()['count']
        db = MySQLdb.connect(host="localhost",user="root",passwd="Davemurray33",db="foodfacts")
        for a in range(max):
            tmp = Category()
            tmp.load(tst.json()['tags'][a])
            print(tmp.name)
            print(a)
            tmp.database_insert(db)
        db.commit()

class Category:
    #categories class

    #def initialisation
    def __init__(self):
        self.name = ''
        self.off_id = ''
        self.elem_count = 0

    #def import single element from OFF API
    def load(self, filepath):
        self.name = unicodedata.normalize('NFKD', filepath['name']).encode('ascii', 'ignore')[:39]
        self.off_id = unicodedata.normalize('NFKD', filepath['id']).encode('ascii', 'ignore')[:39]
        self.elem_count = filepath['products']

    #def insert element in database
    def database_insert(self, database_connection):
        c = database_connection.cursor()
        c.execute("INSERT INTO Categories VALUES (NULL, %s, %s, %s)",
                  (self.name, self.off_id, self.elem_count))



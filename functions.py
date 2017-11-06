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
        self.finest_cat = ''
        self.finest_cat_id = 1
        self.ingredients = ''
        self.grade = 6
        self.brand = ''
        self.stores = ''

    #def import from json
    def jsonread(self, json_file):
        if 'product_name_fr' in json_file:
            self.name = unicodedata.normalize('NFKD', json_file['product_name_fr']).encode('ascii', 'ignore')[:39]
        if 'code' in json_file:
            self.link = 'https://fr.openfoodfacts.org/produit/'+json_file['code']
        if 'ingredients' in json_file:
            self.ingredients = unicodedata.normalize('NFKD', str(json_file['ingredients'])).encode('ascii', 'ignore')
        if 'nutrition_grade_fr' in json_file:
            if json_file['nutrition_grade_fr'] == 'a':
                self.grade = 1
            elif json_file['nutrition_grade_fr'] == 'b':
                self.grade = 2
            elif json_file['nutrition_grade_fr'] == 'c':
                self.grade = 3
            elif json_file['nutrition_grade_fr'] == 'd':
                self.grade = 4
            elif json_file['nutrition_grade_fr'] == 'e':
                self.grade = 5
        if 'brands' in json_file:
            self.brand = unicodedata.normalize('NFKD', json_file['brands']).encode('ascii', 'ignore')[:39]
        if 'sores' in json_file:
            self.stores = unicodedata.normalize('NFKD', json_file['stores']).encode('ascii', 'ignore')[:39]
        if 'categories' in json_file:
            self.categories = json_file['categories'].split(',')
            self.categories = list(map(str.lstrip, self.categories))
            tmp = []
            for cat in self.categories:
                tmp.append(unicodedata.normalize('NFKD', cat).encode('ascii', 'ignore')[:39])
            self.categories = tmp

    #Insertion of the aliment data in db
    def aliment_fill(self, db):
        c = db.cursor()
        #Test if the element is already in the database
        if c.execute("SELECT id FROM Elements WHERE"
                     "(name, link) = (%s, %s)", (self.name, self.link)) == 0:
            #If not, fill the database
            c.execute("INSERT INTO Elements VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)",
                      (self.name, self.link, self.finest_cat_id, self.ingredients, self.grade,
                       self.brand, self.stores))
        db.commit()


    #def insert categories parenthood into database
    def parenthood_fill(self, db):
        c = db.cursor()
        #print(len(self.categories))
        #print(self.categories)
        if len(self.categories) > 1:

            for a in range(len(self.categories) - 1):
                temp = []
                #print(self.categories[a])
                #print(self.categories[a+1])
                c.execute("SELECT id FROM Categories WHERE name IN (%s, %s)"
                          "OR off_id IN (%s, %s)",
                          (self.categories[a], self.categories[a+1], self.categories[a], self.categories[a+1]))

                for id in c:
                    temp.append(id)

                if len(temp) == 2:
                    if c.execute("SELECT category_id FROM Parenthood WHERE"
                                 "(category_id, parent_category_id) = (%s, %s)", (temp[1], temp[0])) == 0:
                        c.execute("INSERT IGNORE INTO Parenthood VALUES (%s, %s)", (temp[1], temp[0]))
            self.finest_cat = self.categories[a+1]
        elif len(self.categories) == 1:
            self.finest_cat = self.categories

            c.execute("SELECT id FROM Categories WHERE name IN (%s, %s)",
                  (self.finest_cat, self.finest_cat))
            for id in c:
                self.finest_cat_id = id

        db.commit()



    #def database_insert(self):

class Categories:

    def overview(self, db):
        #Extracts all the categories from OFF and fills in database
        #Only to be used while generating database
        tst = requests.get('https://fr.openfoodfacts.org/categories.json')
        max = tst.json()['count']

        for a in range(max):
            tmp = Category()
            tmp.load(tst.json()['tags'][a])
            print(tmp.name)
            print(a)
            tmp.database_insert(db)
        c = db.cursor()
        c.execute("DELETE FROM Categories WHERE name = ''")
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

def fillelements(database):
    for a in range(1, 7184):
        link = ('https://world.openfoodfacts.org/country/france/%d.json' %a)
        print(a)
        resp = requests.get(link)
        for element in resp.json()['products']:
            test = Product()
            test.jsonread(element)
            test.parenthood_fill(database)
            test.aliment_fill(database)



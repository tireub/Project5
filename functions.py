import json
import MySQLdb
import requests
import unicodedata
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

from operator import itemgetter

import time


class Product:
    # product class

    # def intialisation
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

    # def import from json
    def jsonread(self, json_file):
        if 'product_name_fr' in json_file:
            self.name = unicodedata.normalize(
                        'NFKD', json_file['product_name_fr']
                        ).encode('ascii', 'ignore')[:39]
        if 'code' in json_file:
            self.link = 'https://fr.openfoodfacts.org/produit/' + \
                        json_file['code']
        if 'ingredients' in json_file:
            self.ingredients = unicodedata.normalize(
                               'NFKD', str(json_file['ingredients'])).encode(
                               'ascii', 'ignore')
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
            self.brand = unicodedata.normalize(
                         'NFKD', json_file['brands']).encode(
                         'ascii', 'ignore')[:39]
        if 'sores' in json_file:
            self.stores = unicodedata.normalize(
                          'NFKD', json_file['stores']).encode(
                          'ascii', 'ignore')[:39]
        if 'categories' in json_file:
            # Separate the categories into a list and nromalise the name
            self.categories = json_file['categories'].split(',')
            self.categories = list(map(str.lstrip, self.categories))
            tmp = []
            for cat in self.categories:
                tmp.append(unicodedata.normalize(
                           'NFKD', cat).encode('ascii', 'ignore')[:39])
            self.categories = tmp

    # Insertion of the aliment data in db
    def aliment_fill(self, db):
        c = db.cursor()
        # Test if the element is already in the database
        if c.execute("SELECT id FROM Elements WHERE"
                     "(name, link) = (%s, %s)", (self.name, self.link)) == 0:
            # If not, fill the database
            c.execute("INSERT INTO Elements VALUES "
                      "(NULL, %s, %s, %s, %s, %s, %s, %s)",
                      (self.name, self.link, self.finest_cat_id,
                       self.ingredients, self.grade,
                       self.brand, self.stores))
        db.commit()

    # def insert categories parenthood into database
    def parenthood_fill(self, db):
        c = db.cursor()
        # Test if we need to fill parenthood
        if len(self.categories) > 1:

            for a in range(len(self.categories) - 1):
                temp = []
                c.execute("SELECT id FROM Categories WHERE name IN (%s, %s)"
                          "OR off_id IN (%s, %s)",
                          (self.categories[a], self.categories[a+1],
                           self.categories[a], self.categories[a+1]))

                for id in c:
                    temp.append(id)

                if len(temp) == 2:
                    if c.execute("SELECT category_id FROM Parenthood WHERE"
                                 "(category_id, parent_category_id) = "
                                 "(%s, %s)",
                                 (temp[1], temp[0])) == 0:
                        # Insertion within database if doesn't already exist
                        c.execute("INSERT IGNORE INTO Parenthood "
                                  "VALUES (%s, %s)",
                                  (temp[1], temp[0]))
            self.finest_cat = self.categories[a+1]
        elif len(self.categories) == 1:
            self.finest_cat = self.categories

            c.execute("SELECT id FROM Categories WHERE name IN (%s, %s)",
                      (self.finest_cat, self.finest_cat))
            for id in c:
                self.finest_cat_id = id

        db.commit()


class Categories:

    def overview(self, db):
        # Extracts all the categories from OFF and fills in database
        # Only to be used while generating database
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
    # categories class

    # def initialisation
    def __init__(self):
        self.name = ''
        self.off_id = ''
        self.elem_count = 0

    # def import single element from OFF API
    def load(self, filepath):
        self.name = unicodedata.normalize(
                    'NFKD', filepath['name']).encode('ascii', 'ignore')[:39]
        self.off_id = unicodedata.normalize(
                      'NFKD', filepath['id']).encode('ascii', 'ignore')[:39]
        self.elem_count = filepath['products']

    # def insert element in database
    def database_insert(self, database_connection):
        c = database_connection.cursor()
        c.execute("INSERT INTO Categories VALUES (NULL, %s, %s, %s)",
                  (self.name, self.off_id, self.elem_count))


def fillelements(database):
    # Fill the database with elements from the Openfoodfacts api
    for a in range(1, 7184):
        link = ('https://world.openfoodfacts.org/country/france/%d.json' % a)
        print(a)
        resp = requests.get(link)
        for element in resp.json()['products']:
            test = Product()
            test.jsonread(element)
            test.parenthood_fill(database)
            test.aliment_fill(database)


class Displayedlist:

    # def initialisation
    def __init__(self):
        self.elems = []
        self.count = 0

    def lvl1load(self, cursor, index):
        # Load list of categories directly from Categories
        temp = []
        cursor.execute("SELECT name, id FROM Categories "
                       "WHERE id > %s LIMIT %s",
                       (index, 20))

        for name in cursor:
            temp.append(name)

        self.elems = temp
        self.count = len(self.elems)

    def lvl2load(self, cursor, id, index):
        # Load sub-categories
        temp = []
        cursor.execute("SELECT name, id FROM Categories "
                       "INNER JOIN Parenthood ON "
                       "Parenthood.category_id = Categories.id WHERE "
                       "Parenthood.parent_category_id = %s ORDER BY id "
                       "LIMIT %s,%s",
                       (id, index, 20))

        for name in cursor:
            temp.append(name)

        self.elems = temp
        self.count = len(self.elems)

    def savedload(self, cursor, index):
        # Retrieve the list of saved searches
        temp = []
        cursor.execute("SELECT Saved1.id AS s_id, "
                       "Saved1.search_date AS s_date, "
                       "Categories.name AS name "
                       "FROM Saved_searches AS saved1 "
                       "INNER JOIN Categories "
                       "ON Saved1.search_id = Categories.id "
                       "LIMIT %s, %s", (index, 20))

        for (s_id, s_date, name) in cursor:
            temp.append([s_id, s_date, name])

        self.elems = temp
        self.count = len(self.elems)


class Results:

    # def initialisation
    def __init__(self):
        self.elems = []
        self.count = 0
        self.used_categories = []
        self.cat_id = []

    def fill_categories(self, cursor, id):
        # Define all categories hierarchically below the selected category
        global new_childs
        self.cat_id = id
        self.used_categories = [id]
        new_elems = [id]

        while new_elems != []:
            new_childs = []
            for elem in new_elems:

                format_str = "SELECT category_id FROM Parenthood " \
                             "WHERE parent_category_id = {id} " \
                             "ORDER BY category_id"

                sql_command = format_str.format(id=elem)
                cursor.execute(sql_command)

                for category_id in cursor:
                    if category_id[0] not in self.used_categories:
                        self.used_categories.append(category_id[0])
                        new_childs.append(category_id[0])

            new_elems = new_childs

    def findelements(self, cursor):
        # Extract all elements of the desired categories from database
        temp = []
        if len(self.used_categories) == 1:
            format_str = "SELECT nutrition_grade, name, brand, stores, " \
                         "link, id " \
                         "FROM Elements WHERE category_id = {list} " \
                         "ORDER BY nutrition_grade"
            sql_command = format_str.format(list=self.used_categories[0])

        else:
            format_str = "SELECT nutrition_grade, name, brand, stores, " \
                         "link, id " \
                         "FROM Elements WHERE category_id IN {list} " \
                         "ORDER BY nutrition_grade"
            sql_command = format_str.format(list=tuple(self.used_categories))

        cursor.execute(sql_command)

        for (nutrition_grade, name, brand, stores, link, id) in cursor:
            self.elems.append([nutrition_grade, name, brand, stores, link, id])

    def table(self):
        # function used to display the results in a table, with color codes
        # NOT WORKING ATM
        py.sign_in('Tireub', 'SteveHarris')

        temp = zip(*self.elems)
        print(list(temp))
        trace = go.Table(
            header=dict(values=['Nutrition grade', 'Name',
                                'Brands', 'Stores', 'Link'],
                        line=dict(color='#7D7F80'),
                        fill=dict(color='#a1c3d1'),
                        align=['left'] * 5),
            cells=dict(values=list(temp),
                       line=dict(color='#7D7F80'),
                       fill=dict(color='#EDFAFF'),
                       align=['left']*5))

        layout = dict(width=500, height=300)
        data = [trace]
        fig = dict(data=data, layout=layout)
        py.iplot(fig, filename='styled_table')

    def save_search(self, cursor):
        # Save within database
        elems_id = list(map(itemgetter(5), self.elems))
        cursor.execute("INSERT INTO Saved_searches VALUES "
                       "(NULL, %s, %s, %s)",
                       (datetime.datetime.now().date(),
                        self.cat_id, str(elems_id)))

    def load_from_save(self, cursor, id):
        # Load elements with a save id
        format_str = ("SELECT search_replacement FROM Saved_searches "
                      "WHERE id = {search_id}")
        sql_command = format_str.format(search_id=id)
        cursor.execute(sql_command)
        for search_replacement in cursor:
            elems_id = search_replacement

        id_list = elems_id[0]

        elems_id_num = [int(id_list.split()[0][1:-1])]

        for a in id_list.split()[1:]:
            elems_id_num.append(int(a[:-1]))

        format_str = "SELECT nutrition_grade, name, brand, stores, " \
                     "link, id " \
                     "FROM Elements WHERE id IN {list} " \
                     "ORDER BY nutrition_grade"
        sql_command = format_str.format(list=tuple(elems_id_num))

        cursor.execute(sql_command)

        for (nutrition_grade, name, brand, stores, link, id) in cursor:
            self.elems.append([nutrition_grade, name, brand, stores, link, id])

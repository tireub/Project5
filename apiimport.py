import json
import requests
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

from Functions import*
from operator import itemgetter

'''
MAIN
'''

# Connection to database
db = MySQLdb.connect(host="localhost", user="root", passwd="Davemurray33",
                     db="foodfacts")
c = db.cursor()

# Initialisation
cat_list = Displayedlist()
results = Results()
main_loop = True

# Intro message
welcome_message = "Bienvenue sur la plate-forme Pur Beurre. \n" \
                  "Vous pouvez à tout moment quitter en tapant exit \n" \
                  "Pour revenir à la page précédente, tapez retour \n"
print (welcome_message)

# Main loop
while main_loop is True:
    message = ("1: Quel aliment souhaitez-vous remplacer ?\n"
               "2: Retrouver mes aliments substitués.\n")
    choice_1 = input(message)
    if choice_1 == 'exit':
            quit()
            # This will stop the program!

    elif choice_1 == "1":
        index1 = 2
        # Second choice loop
        while main_loop is True:
            # load diasplay list
            cat_list.lvl1load(c, index1)
            message_2 = ('\nSelectionnez la catégorie désirée: \n\n' +
                         '\n'.join('{}: {}'.format(*k)
                                   for k in enumerate(map(itemgetter(0),
                                                          cat_list.elems))) +
                         '\n\n20: Afficher plus de choix\n')
            choice_2 = input(message_2)

            if choice_2 == 'exit':
                quit()

            elif choice_2 == '20':
                if cat_list.count == 20:
                    index1 += 20
                else:
                    index1 = 2

            elif choice_2 == 'retour':
                break

            elif choice_2.isdigit() and int(choice_2) < cat_list.count:
                # choice 3 loop
                index2 = 0
                while main_loop is True:
                    cat_list.lvl2load(c, int(choice_2) + 1 + index1, index2)

                    message_3 = ('\nSelectionnez la catégorie désirée: \n\n' +
                                 '\n'.join('{}: {}'.format(*k) for k in
                                           enumerate(map(itemgetter(0),
                                                         cat_list.elems))) +
                                 '\n\n20: Afficher plus de choix\n' +
                                 '*categorie: Afficher les sous-catégories\n')
                    choice_3 = input(message_3)

                    if choice_3 == 'exit':
                        quit()

                    elif choice_3 == 'retour':
                        break

                    elif choice_3 == '20':
                        if cat_list.count == 20:
                            index2 += 20
                        else:
                            index2 = 0

                    # Ability to go deeper within the sub categories
                    elif '*' in choice_3:
                        index3 = 0
                        temp_id = cat_list.elems[int(choice_3.strip('*'))]

                        while True:
                            cat_list.lvl2load(c, temp_id[1], index3)

                            message_3 = (
                                '\nSelectionnez la catégorie désirée: \n\n' +
                                '\n'.join('{}: {}'.format(*k)
                                          for k in enumerate(
                                    map(itemgetter(0), cat_list.elems))))
                            choice = input(message_3)

                            if choice == 'exit':
                                quit()

                            elif choice == 'retour':
                                break

                            elif choice.isdigit() and int(
                                 choice) < cat_list.count:
                                results.fill_categories(
                                    c, cat_list.elems[int(choice)][1])
                                results.findelements(c)
                                main_loop = False

                    elif choice_3.isdigit() and int(choice_3) < cat_list.count:
                        results.fill_categories(
                            c, cat_list.elems[int(choice_3)][1])
                        results.findelements(c)
                        main_loop = False

    elif choice_1 == "2":
        # retrieve saved searchesinput
        search_index = 0

        while main_loop is True:
            # load search history
            cat_list.savedload(c, search_index)
            message = ('\nSelectionnez la sauvegarde désirée: \n\n' +
                       '\n'.join('{}: {}'.format(*k)
                                 for k in enumerate(map(itemgetter(1, 2),
                                                        cat_list.elems))) +
                       '\n\n20: Afficher plus de choix\n')
            choice = input(message)

            if choice == 'exit':
                quit()

            elif choice.isdigit() and int(choice) < cat_list.count:
                results.load_from_save(c, cat_list.elems[int(choice)][0])
                main_loop = False


# Results loop
while True:
    # results.table(). Still to implement
    result_message = ('\nRésultats de la recherche:\n\n' +
                      '\n'.join('{}: {}'.format(*k) for k in
                                enumerate(results.elems)) +
                      '\n\nSave: Sauvegarder la recherche\n')
    result_choice = input(result_message)

    if result_choice == 'Save':
        results.save_search(c)
        db.commit()
        break

    elif result_choice == 'exit':
        quit()

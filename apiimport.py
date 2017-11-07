import json
import requests

from Functions import*

'''
MAIN
'''

# Connection to database
db = MySQLdb.connect(host="localhost", user="root", passwd="Davemurray33",
                     db="foodfacts")
c = db.cursor()

# Initialisation
cat_list = Displayedlist()

# Intro message
welcome_message = "Bienvenue sur la plate-forme Pur Beurre. \n" \
                  "Vous pouvez à tout moment quitter en tapant exit \n" \
                  "Pour revenir à la page précédente, tapez retour \n"
print (welcome_message)

# Main loop
while True:
    message = ("1: Quel aliment souhaitez-vous remplacer ?\n"
               "2: Retrouver mes aliments substitués.\n")
    choice_1 = input(message)
    if choice_1 == 'exit':
            quit()
            # This will stop the program!

    elif choice_1 == "1":
        index1 = 2
        # Second choice loop
        while True:
            # load diasplay list
            cat_list.lvl1load(c, index1)
            message_2 = ('Selectionnez la catégorie désirée: \n\n' + '\n'.join(
                        '{}: {}'.format(*k) for
                        k in enumerate(cat_list.elems)) +
                         '\n20: Afficher plus de choix\n')
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

            elif int(choice_2) < 20:
                # choice 3 loop
                index2 = 0
                while True:
                    cat_list.lvl2load(c, int(choice_2) + 1 + index1, index2)

                    message_3 = ('Selectionnez la catégorie désirée: \n\n' +
                                 '\n'.join('{}: {}'.format(*k) for k in
                                           enumerate(cat_list.elems)) +
                                 '\n20: Afficher plus de choix\n')
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

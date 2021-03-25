import sys
import time
import os
import re
import whois

# coding : utf-8

COLORS = {
    "black": "\u001b[30;1m",
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "lightgreen": "\u001b[38;5;82m",
    "lightyellow": "\u001b[38;5;226m",
    "yellow": "\u001b[33;1m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "yellow-background": "\u001b[43m",
    "black-background": "\u001b[40m",
    "cyan-background": "\u001b[46;1m",
}

asciidraw = "\n[[lightyellow]] _ _ _     _      _____         _         _   \n| | | |___| |_   |  _  |___ ___| |_ _ ___| |_ \n| | | | -_| . |  |     |   | .'| | | |_ -|  _|\n|_____|___|___|  |__|__|_|_|__,|_|_  |___|_|  \n                                 |___|        \nAuthor : @Coroxx on github\n"


def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


def lang():
    global language
    global asciidraw
    os.system("clear")
    response = input(
        colorText("[[yellow]]Language/Langue :\n\n[1] French\n[2] English \n\nChoice : "))
    if response == "1":
        language = "fr"
        main_FR()
    elif response == "2":
        language = "ang"
        main_ANGw()
    else:
        print(colorText("[[red]]\n[!] Incorrect choice, try again"))
        time.sleep(2)
        lang()


try:
    import requests
    from bs4 import BeautifulSoup
    import urllib
    from urllib.request import urlopen
except:
    os.system("clear")
    if language == "fr":
        print(
            colorText(
                "[[red]]Tu n'a pas correctement réalisé l'installation, laisse moi le faire pour toi.."
            )
        )
        time.sleep(2)
    elif language == "ang":
        print(
            colorText(
                "[[red]]You didn't do the installation correctly, let me do it for you..."
            )
        )
        time.sleep(2)
    try:
        os.system("pip install -r requirements.txt")
        os.system("clear")
        print(colorText("[[green]]Succes !"))
        time.sleep(2)
    except:
        os.system("clear")
        time.sleep(1)
        print(
            colorText(
                "[[red]]Uh, an error has occurred, please report the problem on github."
            )
        )


def parameters_FR():
    settings = []
    global request
    link = str(input(colorText(
        "[[white]]\nLien de la page (doit commencer par https/http): ")))
    if (bool(re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=])*', link))):
        try:
            request = requests.get(link, timeout=5)
            print(colorText('[[green]][+] Ajouté !'))
            settings.append(link)
        except:
            print(colorText('\n[[red]][-] Le site ne réponds pas..'))
            time.sleep(2)
            parameters_FR()
    else:
        print(colorText('[[red]][!] Syntaxe incorrecte !'))
        time.sleep(2)
        parameters_FR()
    whoisresult = input(colorText(
        '[[yellow]]\n[?] Voulez-vous analyser le domaine automatiquement à l\'aide de whois ? (y/n): '))
    if (bool(re.match(r"OUI|oui|y(?:es)?|Y", whoisresult))):
        settings.append(True)
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", whoisresult))):
        settings.append(False)
    time.sleep(2)
    print(colorText('\n[[green]][+] Démarrage de l\'analyse...'))

    result = parser(link, whois)

    time.sleep(1)

    os.system('clear')
    if whoisresult:
        if 'https://' in link:
            whoisresult = whois.query(link.replace('https://', ''))
        elif 'http://' in link:
            whoisresult = whois.query(link.replace('http://', ''))
        print(colorText('[[blue]]\nWhois : '),
              '\n\nDate d\'expiration du domaine :', whoisresult.expiration_date,
              '\nDate de création du domaine :', whoisresult.creation_date,
              '\nNom : ', whoisresult.registrar,
              '\nDernière mise à jour : ', whoisresult.last_updated)

    time.sleep(2)
    print(colorText('[[green]]\n\n--Résultats--'),
          '\n\n\nNombre de très grands titres (h1) : ', result[3],
          '\nNombre de grands titres (h2) : ', result[4],
          '\nNombre de titres moyens (h3) : ', result[5],
          '\nNombre de titres (h4) : ', result[6],
          '\nNombre de textes <p> : ', result[7],
          '\nNombre de liens <a> : ', result[1],
          '\nNombre d\'image <img>: ', result[2],
          '\nNombre de <div> : ', result[0],
          '\nNombre de total de balises de texte : ', result[7],
          '\nNombre de champs <input> : ', result[8],
          '\nNombre de boutons <button> : ', result[9],
          '\nNombre de formulaires <form> : ', result[10])
    time.sleep(2)
    if result[11]:
        varcount = request.text.count('var')
        functioncount = request.text.count('function')
        print(
            colorText('\n[[cyan]][+] Javascript est détecté sur cette page avec un total de {} variables déclarées\nNombre de fonction(s) : {}').format(varcount, functioncount))
    else:
        print(
            colorText('[[red]]\n[-] Aucun javascript n\'est présent sur cette page\n'))
    customquestion = input(colorText(
        '[[yellow]]\n[?] Voulez-vous ajouter des balises html à rechercher ? (Séparées d\'une virgule, exemple : <span, <footer, ...) : '))
    customs = customquestion.split(",")
    if customquestion == '':
        customs = False
    if customs:
        print(colorText('[[yellow]]\n\n--Custom--\n'))
        for custom in customs:
            resultcustom = request.text.count(str(custom))
            print(colorText('Nombre total de '),
                  custom, ': ', resultcustom)
    customs = []
    again = input(colorText(
        '[[yellow]]\n[?] Voulez-vous analyser un nouveau domaine ? (y/n): '))
    if (bool(re.match(r"OUI|oui|y(?:es)?|Y", again))):
        parameters_FR()
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", again))):
        os.system('clear')
        print(colorText('\n[[red]][!] Retour au terminal... '))
        sys.exit()


def parameters_US():
    global request
    link = str(input(colorText(
        "[[white]]\nPage link (must start with https/http): ")))
    if (bool(re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=])*', link))):
        try:
            request = requests.get(link, timeout=5)
            print(colorText('[[green]][+] Succes !'))
        except:
            print(colorText('\n[[red]][-] The site has timeout ..'))
            time.sleep(2)
            parameters_US()
    else:
        print(colorText('[[red]][!] Incorrect syntax !'))
        time.sleep(2)
        parameters_US()
    whoisresult = input(colorText(
        '[[yellow]]\n[?] Do you want to scan the domain using whois? (y/n): '))
    if (bool(re.match(r"OUI|oui|y(?:es)?|Y", whoisresult))):
        whoisresult = True
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", whoisresult))):
        whoisresult = False
    else:
        print(colorText('[[red]][!] Incorrect choice'))
        time.sleep(2)
        parameters_US()
    time.sleep(2)
    print(colorText('\n[[green]][+] Starting the analysis...'))
    time.sleep(1)

    result = parser(link, whois)

    time.sleep(1)

    os.system('clear')
    if whoisresult:
        if 'https://' in link:
            whoisresult = whois.query(link.replace('https://', ''))
        elif 'http://' in link:
            whoisresult = whois.query(link.replace('http://', ''))
        print(colorText('[[blue]]\nWhois : '),
              '\n\nDomain expiration date :', whoisresult.expiration_date,
              '\nDomain creation date:', whoisresult.creation_date,
              '\nServer : ', whoisresult.registrar,
              '\nLastest update: ', whoisresult.last_updated)

    time.sleep(2)
    print(colorText('[[green]]\n\n--Résultats--'),
          '\n\n\nNumber of very large titles (h1) : ', result[3],
          '\nNumber of major titles (h2) : ', result[4],
          '\nNumber of medium-sized titles (h3) : ', result[5],
          '\nNumber of titles (h4) : ', result[6],
          '\nNumber of texts <p> : ', result[7],
          '\nNumber of links <a> : ', result[1],
          '\nNumber of images <img>: ', result[2],
          '\nNumber of div <div> : ', result[0],
          '\nTotal number of text tags : ', result[7],
          '\nNumber of <input> fields : ', result[8],
          '\nNumber of buttons <button> : ', result[9],
          '\nNumber of forms <form> <form> : ', result[10])
    time.sleep(2)
    if result[11]:
        varcount = request.text.count('var')
        functioncount = request.text.count('function')
        print(
            colorText('\n[[cyan]][+] Javascript is detected on this page with a total of {} variables declared\nNumber of function(s) : {}').format(varcount, functioncount))
    else:
        print(
            colorText('[[red]]\n[-] No javascript is present on this page\n'))
    customquestion = input(colorText(
        '[[yellow]]\n[?] Do you want to add html tags to search? (Separated by a comma, example : <span, <footer, ...) : '))
    customs = customquestion.split(",")
    if customquestion == '':
        customs = False
    if customs:
        print(colorText('[[yellow]]\n\n--Custom--\n'))
        for custom in customs:
            resultcustom = request.text.count(str(custom))
            print(colorText('Number of '),
                  custom, ': ', resultcustom)
    customs = []
    again = input(colorText(
        '[[yellow]]\n[?] Do you want to analyse a new domain? (y/n): '))
    if (bool(re.match(r"OUI|oui|y(?:es)?|Y", again))):
        parameters_FR()
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", again))):
        os.system('clear')
        print(colorText('\n[[red]][!] Exiting... '))
        sys.exit()


def parser(url, whois):
    global request
    counts = []

    counts.append((request.text.count('<div')))
    counts.append((request.text.count('<a')))
    counts.append((request.text.count('<img')))
    counts.append((request.text.count('<h1')))
    counts.append((request.text.count('<h2')))
    counts.append((request.text.count('<h3')))
    counts.append((request.text.count('<h4')))
    counts.append((request.text.count('<h4') + request.text.count('<h3') +
                  request.text.count('<h2') + request.text.count('<h1') + request.text.count('<p')))
    counts.append((request.text.count('<input')))
    counts.append((request.text.count('<button')))
    counts.append((request.text.count('<form')))
    if '<script' in request.text:
        counts.append(True)
    else:
        counts.append(False)
    return counts


def main_ANG():
    global asciidraw
    os.system("clear")
    print(colorText(asciidraw),
          "\n[1] Analyse a web page\n[2] Langue/Langage\n\n\n[3] Exit")
    choice = input("\nChoix : ")
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Incorrect choice !\n'))
        time.sleep(2)
        os.system('clear')
        main_ANG()
    if (choice == 1):
        parameters_FR()
    elif(choice == 2):
        lang()
    elif(choice == 3):
        print(colorText('[[red]]\n[!] Exiting..'))
        time.sleep(1)
        sys.exit()
    else:
        print(colorText('[[red]]\n[!] Incorrect choice !\n'))
        time.sleep(2)
        main_ANG()


def main_FR():
    global asciidraw
    os.system("clear")
    print(colorText(asciidraw),
          "\n[1] Analyser une page web\n[2] Langue/Langage\n\n\n[3] Quitter")
    choice = input("\nChoix : ")
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Choix incorrect !\n'))
        time.sleep(2)
        os.system('clear')
        main_FR()
    if (choice == 1):
        parameters_FR()
    elif(choice == 2):
        lang()
    elif(choice == 3):
        print(colorText('[[red]]\n[!] Retour au terminal...'))
        sys.exit()
    else:
        print(colorText('[[red]]\n[!] Choix incorrect !\n'))
        time.sleep(2)
        main_FR()


if __name__ == '__main__':
    lang()

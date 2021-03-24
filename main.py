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
    global lang
    global asciidraw
    os.system("clear")
    response = input(
        colorText("[[yellow]]Language/Langue :\n\n[1] French\n[2] English \n\nChoice : "))
    if response == "1":
        lang = "fr"
    elif response == "2":
        lang = "ang"
    else:
        print(colorText("[[red]]\n[!] Incorrect choice, try again"))
        time.sleep(2)
        lang()


lang()

try:
    import requests
    from bs4 import BeautifulSoup
    import urllib
    from urllib.request import urlopen
except:
    os.system("clear")
    if lang == "fr":
        print(
            colorText(
                "[[red]]Tu n'a pas correctement réalisé l'installation, laisse moi le faire pour toi.."
            )
        )
        time.sleep(2)
    elif lang == "ang":
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
        whoisresult = whois.query(link)
        print(colorText('[[blue]]Whois : '),
              '\n\nDate d\'expiration du domaine :', whoisresult.expiration_date,
              '\nDate de création du domaine :', whoisresult.creation_date,
              '\nNom : ', whoisresult.registrar,
              '\nDernière mise à jour : ', whoisresult.last_updated)

    time.sleep(2)
    print(colorText('[[green]]--Résultats--'),
          '\n\n\n Nombre de titres : ', result[3],
          '\nNombre de liens : ', result[1],
          '\nNombre d\'image : ', result[2],
          '\nNombre de div : ', result[0],
          '\nNombre de formulaires : ', result[4])
    time.sleep(2)
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
    whois = input(colorText(
        '[[yellow]]\n[?] Do you want to scan the domain using whois? (y/n): '))
    if (bool(re.match(r"OUI|oui|y(?:es)?|Y", whois))):
        whois = True
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", whois))):
        whois = False
    else:
        print(colorText('[[red]][!] Incorrect choice'))
        time.sleep(2)
        parameters_US()
    time.sleep(2)
    print(colorText('\n[[green]][+] Starting the analysis...'))
    time.sleep(1)

    parser(link, whois)

    return link


def parser(url, whois):
    global request
    counts = []

    counts.append((request.text.count('<div')))
    counts.append((request.text.count('<a')))
    counts.append((request.text.count('<img')))
    counts.append((request.text.count('<h')))
    counts.append((request.text.count('<form')))
    if '<script' in request.text:
        counts.append(True)
    else:
        counts.append(False)
    return counts


def main_ANG():
    pass


def main_FR():
    global asciidraw
    os.system("clear")
    print(colorText(asciidraw), "\n[1] Analyser une page web\n\n[2] Quitter")
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
        print(colorText('[[red]]\n[!] Retour au terminal...'))
        sys.exit()
    else:
        print(colorText('[[red]]\n[!] Choix incorrect !\n'))
        time.sleep(2)
        main_FR()


main_FR()

print()

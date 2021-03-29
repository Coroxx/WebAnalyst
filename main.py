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

asciidraw = "\n[[lightyellow]] _ _ _     _      _____         _         _   \n| | | |___| |_   |  _  |___ ___| |_ _ ___| |_ \n| | | | -_| . |  |     |   | .'| | | |_ -|  _|\n|_____|___|___|  |__|__|_|_|__,|_|_  |___|_|  \n                                 |___|        \nVersion : 1.1\nAuthor : @Coroxx on github\n"


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
        main_ANG()
    else:
        print(colorText("[[red]]\n[!] Incorrect choice, try again"))
        time.sleep(2)
        lang()


try:
    import requests
    from bs4 import BeautifulSoup
    import urllib
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
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
    global completelink

    completelink = str(input(colorText(
        "[[white]]\nLien de la page (doit commencer par https/http): ")))
    if (bool(re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=])*', completelink))):
        try:
            request = requests.get(completelink, timeout=5)
            print(colorText('[[green]][+] Ajouté !'))
            settings.append(completelink)
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
        whoisresult = True
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", whoisresult))):
        whoisresult = False
    else:
        print(colorText('[[red]][!] Choix incorrect !'))
        time.sleep(1)
        parameters_FR()
    time.sleep(2)
    print(colorText('\n[[green]][+] Démarrage de l\'analyse...'))

    result = parser(completelink, whois)

    time.sleep(1)

    os.system('clear')
    if whoisresult:
        link = re.findall(
            r'^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)', completelink)
        whoisresults = whois.query(link[0])
        print(colorText('[[blue]]\nWhois : '),
              '\n\nDate d\'expiration du domaine :', whoisresults.expiration_date,
              '\nDate de création du domaine :', whoisresults.creation_date,
              '\nNom : ', whoisresults.registrar,
              '\nDernière mise à jour : ', whoisresults.last_updated)

    time.sleep(2)
    print(colorText('[[green]]\n\n--Résultats--'),
          '\n\n\nNombre de très grands titres (h1) : ', result[0],
          '\nNombre de grands titres (h2) : ', result[1],
          '\nNombre de titres moyens (h3) : ', result[2],
          '\nNombre de titres (h4) : ', result[3],
          '\nNombre de textes <p> : ', result[4],
          '\nNombre de liens <a> : ', result[5],
          '\nNombre d\'image <img> et <svg>: ', result[6],
          '\nNombre de <div> : ', result[7],
          '\nNombre de champs <input> : ', result[8],
          '\nNombre de boutons <button> : ', result[9],
          '\nNombre de formulaires <form> : ', result[10],
          '\nNombre de listes <ul> et <ol> : ', result[11],
          '\nNombre d\'élements de listes <li>: ', result[12])
    time.sleep(2)
    if result[14] >= 1:
        js = BeautifulSoup(request.text, 'html.parser')
        js = js.find_all('script')
        varcount = 0
        functioncount = 0
        conditioncount = 0
        for balise in js:
            try:
                varcount += balise.count('var')
            except:
                pass
            try:
                functioncount += balise.count('function')
            except:
                pass
            try:
                conditioncount += balise.count(
                    'if(') + balise.count('else(') + balise.count('else if(') + balise.count(
                    'if (') + balise.count('else (') + balise.count('else if (')
            except:
                pass
        print(
            colorText('\n[[cyan]][+] Javascript est détecté sur cette page avec un total de {} variables déclarées\nNombre de fonction(s) : {}\nNombre de condition(s) : {}').format(varcount, functioncount, conditioncount))
        print(
            colorText('[[cyan]]\n[+] Vérification d\'éventuels fichiers javascript tiers...\n'))
        time.sleep(1)

        for src in soup.find_all('script'):
            if src.get('src') == None:
                continue
            if 'https://' in src.get('src') or 'http://' in src.get('src'):
                linkk = src.get('src')
            elif src.get('src').startswith('/'):
                linkk = completelink + src.get('src')
            else:
                linkk = completelink + '/' + src.get('src')
            print(colorText('[[green]][+] Fichier détecté :'),
                  src.get('src'), '\n')
            javascriptrequest = requests.get(linkk)
            javascript = BeautifulSoup(javascriptrequest.text, 'html.parser')
            print(javascript)
            linkk = ''
            functioncount = 0
            for i in javascript.find_all('function'):
                functioncount += 1
            print(colorText('[[cyan]]Nombre de functions : '), functioncount)
            conditioncount = 0
            for i in javascript.find_all(['if', 'if(', 'else if (', 'else if(', 'else(', 'else (']):
                conditioncount += 1
            print(colorText('[[cyan]]Nombre de functions : '),
                  conditioncount, '\n')

    else:
        print(
            colorText('[[red]]\n[-] Aucun javascript n\'est présent sur cette page\n'))
    if result[13] >= 1:
        print(colorText(
            '[[magenta]]\n\n[+] CSS Framework detected ! (TailWind CSS integrated by CDN)\n'))
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
    completelink = str(input(colorText(
        "[[white]]\nPage link (must start with https/http): ")))
    if (bool(re.match(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=])*', completelink))):
        try:
            request = requests.get(completelink, timeout=5)
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

    result = parser(completelink, whois)

    time.sleep(1)

    os.system('clear')
    if whoisresult:
        link = re.findall(
            r'^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n?]+)', completelink)
        whoisresults = whois.query(link[0])
        print(colorText('[[blue]]\nWhois : '),
              '\n\nDomain expiration date :', whoisresults.expiration_date,
              '\nDomain creation date:', whoisresults.creation_date,
              '\nServer : ', whoisresults.registrar,
              '\nLastest update: ', whoisresults.last_updated)
    time.sleep(2)
    print(colorText('[[green]]\n\n--Results--'),
          '\n\n\nNumber of very large titles (h1) : ', result[0],
          '\nNumber of major titles (h2) : ', result[1],
          '\nNumber of medium-sized titles (h3) : ', result[2],
          '\nNumber of titles (h4) : ', result[3],
          '\nNumber total of texts <p> & <h1.... : ', result[4],
          '\nNumber of links <a> : ', result[5],
          '\nNumber of images <img> and <svg> : ', result[6],
          '\nNumber of div <div> : ', result[7],
          '\nNumber of <input> fields : ', result[8],
          '\nNumber of buttons <button> : ', result[9],
          '\nNumber of forms <form> : ', result[10]),
    '\nNumber of lists <ul> and <ol> : ', result[11],
    '\nNumber of list items : ', result[12]
    time.sleep(2)
    if result[14] >= 1:
        varcount = request.text.count('var')
        functioncount = request.text.count('function')
        conditioncount = request.text.count(
            'if(') + request.text.count('else(') + request.text.count('else if(') + request.text.count(
            'if (') + request.text.count('else (') + request.text.count('else if (')
        print(
            colorText('\n[[cyan]][+] Javascript is detected on this page with a total of {} variables declared\nNumber of function(s) : {}\nNumber of condition(s) : {}').format(varcount, functioncount, conditioncount))
    else:
        print(
            colorText('[[red]]\n[-] No javascript is present on this page\n'))
    if result[13] >= 1:
        print(colorText(
            '[[magenta]][+] CSS Framework dedected ! (Tailwind CSS integrated by CDN) '))
    customquestion = input(colorText(
        '[[yellow]]\n[?] Do you want to add html tags to search? (Separated by a comma, format example : <span, <footer, ...) : '))
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
        parameters_US()
    elif (bool(re.match(r"N(?:ON)?|n(?:on?)?", again))):
        os.system('clear')
        print(colorText('\n[[red]][!] Exiting... '))
        sys.exit()


def parser(url, whois):
    global soup
    global request
    counts = []

    counts.append((request.text.count('<h1')))
    counts.append((request.text.count('<h2')))
    counts.append((request.text.count('<h3')))
    counts.append((request.text.count('<h4')))
    counts.append((request.text.count('<h4') + request.text.count('<h3') +
                  request.text.count('<h2') + request.text.count('<h1') + request.text.count('<p')))
    counts.append((request.text.count('<a')))
    counts.append((request.text.count('<img')) + (request.text.count('<svg')))
    counts.append((request.text.count('<div')))
    counts.append((request.text.count('<input')))
    counts.append((request.text.count('<button')))
    counts.append((request.text.count('<form')))
    counts.append((request.text.count('<ul')) + (request.text.count('<ol')))
    counts.append((request.text.count('<li')))
    counts.append((request.text.count('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">')))
    counts.append((request.text.count('<script')))

    soup = BeautifulSoup(request.text, 'html.parser')
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
        parameters_US()
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
